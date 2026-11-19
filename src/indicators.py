"""Calcul des indicateurs de prix (entrées au format D-11)."""

import pandas as pd

COL_STATION = "id_station"
COL_DEPARTEMENT = "departement"
COL_IMPLANTATION = "implantation"
COL_DATE = "date_releve"
COL_PRIX = "prix_gazole"


def prix_hebdo_par_station(historique: pd.DataFrame) -> pd.DataFrame:
    """Prix moyen hebdomadaire par station, sur une grille temporelle commune.

    Entrée : historique nettoyé (D-11). Responsable : Samuel.
    Sortie : id_station, departement, implantation, semaine, prix_hebdo (€/L).
    resample("W") regroupe du lundi au dimanche et date les semaines du dimanche.
    """
    historique = historique.copy()
    historique[COL_DATE] = pd.to_datetime(historique[COL_DATE])

    prix_hebdo = (
        historique.set_index(COL_DATE)
        .groupby(COL_STATION)[COL_PRIX]
        .resample("W")
        .mean()
        .reset_index()
        .rename(columns={COL_DATE: "semaine", COL_PRIX: "prix_hebdo"})
    )

    metadonnees = historique.assign(
        semaine=historique[COL_DATE].dt.to_period("W-SUN").dt.end_time.dt.normalize()
    )
    metadonnees = metadonnees.sort_values(COL_DATE, kind="stable").drop_duplicates(
        [COL_STATION, "semaine"], keep="last"
    )[[COL_STATION, "semaine", COL_DEPARTEMENT, COL_IMPLANTATION]]
    prix_hebdo = pd.merge_asof(
        prix_hebdo.sort_values("semaine"),
        metadonnees.sort_values("semaine"),
        on="semaine",
        by=COL_STATION,
        direction="backward",
    )
    return prix_hebdo.sort_values([COL_STATION, "semaine"])[
        [COL_STATION, COL_DEPARTEMENT, COL_IMPLANTATION, "semaine", "prix_hebdo"]
    ].reset_index(drop=True)


def prix_median_hebdo(prix_hebdo: pd.DataFrame) -> pd.DataFrame:
    """Prix médian hebdomadaire de la région, en €/L (QA-4.1).

    Entrée : sortie de prix_hebdo_par_station(). Responsable : Samuel.
    Sortie : semaine, prix_median (€/L), nb_stations.
    """
    median_par_semaine = prix_hebdo.groupby("semaine").agg(
        prix_median=("prix_hebdo", "median"),
        nb_stations=("prix_hebdo", "count"),
    )
    return median_par_semaine.reset_index()


def prix_median_par_departement(prix_hebdo: pd.DataFrame) -> pd.DataFrame:
    """Prix médian par département, écart en cts et en % (QA-1.1).

    Entrée : sortie de prix_hebdo_par_station(). Responsable : Samuel.
    Écart de chaque département au moins cher ; le plus grand écart de la
    colonne est l'écart entre le moins cher et le plus cher.
    """
    par_station = prix_hebdo.groupby([COL_STATION, COL_DEPARTEMENT]).agg(
        prix_station=("prix_hebdo", "median")
    )
    par_station = par_station.reset_index()

    par_departement = par_station.groupby(COL_DEPARTEMENT).agg(
        prix_median=("prix_station", "median"),
        nb_stations=(COL_STATION, "nunique"),
    )
    par_departement = par_departement.reset_index()

    moins_cher = par_departement["prix_median"].min()
    ecart = par_departement["prix_median"] - moins_cher
    par_departement["ecart_cts"] = ecart * 100
    par_departement["ecart_pct"] = ecart / moins_cher * 100
    par_departement["prix_median"] = par_departement["prix_median"].round(3)
    par_departement[["ecart_cts", "ecart_pct"]] = par_departement[
        ["ecart_cts", "ecart_pct"]
    ].round(2)
    return par_departement

# --- Axe QA-1 (Hafsa) ---


def ecart_departements_au_75(prix_hebdo: pd.DataFrame) -> pd.DataFrame:
    """Écart de prix médian de chaque département au 75, année par année (QA-1.1, H-2).

    Entrée : sortie de prix_hebdo_par_station() issue de la table jointe (D-18 appliquée).
    Sortie : DataFrame avec annee, departement, prix_median, nb_stations,
    écarts au 75 (cts/L, %, €/100L) et écart au moins cher (cts/L, %).
    """
    df = prix_hebdo.copy()
    df[COL_DEPARTEMENT] = df[COL_DEPARTEMENT].astype(str)
    df["annee"] = pd.to_datetime(df["semaine"]).dt.year

    resultats = []
    for annee, groupe in df.groupby("annee"):
        stats = prix_median_par_departement(groupe)
        ligne_75 = stats.loc[stats[COL_DEPARTEMENT] == "75", "prix_median"]
        if ligne_75.empty:
            continue

        prix_75 = ligne_75.iloc[0]
        ecart = stats["prix_median"] - prix_75

        stats["annee"] = annee
        stats["ecart_75_cts"] = (ecart * 100).round(2)
        stats["ecart_75_pct"] = (ecart / prix_75 * 100).round(2)
        # D-09 : 1 ct/L équivaut à 1 € pour 100 L
        stats["ecart_75_eur_100l"] = stats["ecart_75_cts"]

        resultats.append(stats)

    if not resultats:
        return pd.DataFrame()

    colonnes = [
        "annee",
        COL_DEPARTEMENT,
        "prix_median",
        "nb_stations",
        "ecart_75_cts",
        "ecart_75_pct",
        "ecart_75_eur_100l",
        "ecart_cts",
        "ecart_pct",
    ]
    return pd.concat(resultats, ignore_index=True)[colonnes]


def prix_median_par_commune(
    historique_joint: pd.DataFrame, min_stations: int = 5
) -> pd.DataFrame:
    """Prix médian par commune pour les communes ayant au moins `min_stations` (QA-1.2).

    Entrée : table jointe nettoyée (historique_joint_idf.parquet, D-18 appliquée).
    Sortie : departement, ville, prix_median (€/L), nb_stations,
    ecart_med_reg_cts, ecart_med_reg_eur_100l, trié par prix croissant.
    """
    prix_hebdo = prix_hebdo_par_station(historique_joint)

    villes = (
        historique_joint[[COL_STATION, "ville"]]
        .dropna(subset=["ville"])
        .drop_duplicates(subset=[COL_STATION], keep="last")
    )

    par_station = (
        prix_hebdo.groupby([COL_STATION, COL_DEPARTEMENT])
        .agg(prix_station=("prix_hebdo", "median"))
        .reset_index()
        .merge(villes, on=COL_STATION, how="inner")
    )

    mediane_regionale = par_station["prix_station"].median()

    par_commune = (
        par_station.groupby([COL_DEPARTEMENT, "ville"])
        .agg(
            prix_median=("prix_station", "median"),
            nb_stations=(COL_STATION, "nunique"),
        )
        .reset_index()
    )

    par_commune = par_commune[par_commune["nb_stations"] >= min_stations].copy()
    ecart_reg = par_commune["prix_median"] - mediane_regionale
    par_commune["ecart_med_reg_cts"] = (ecart_reg * 100).round(2)
    # D-09 : 1 ct/L équivaut à 1 € pour 100 L
    par_commune["ecart_med_reg_eur_100l"] = par_commune["ecart_med_reg_cts"]
    par_commune["prix_median"] = par_commune["prix_median"].round(3)

    colonnes = [
        COL_DEPARTEMENT,
        "ville",
        "prix_median",
        "nb_stations",
        "ecart_med_reg_cts",
        "ecart_med_reg_eur_100l",
    ]
    return (
        par_commune[colonnes]
        .sort_values("prix_median", ascending=True)
        .reset_index(drop=True)
    )


def dispersion_par_departement(
    prix_hebdo: pd.DataFrame, par_annee: bool = False
) -> pd.DataFrame:
    """Dispersion intra-départementale des prix médians par station (QA-1.3).

    Entrée : sortie de prix_hebdo_par_station() issue de la table jointe (D-18 appliquée).
    Si par_annee=True, le calcul est effectué année par année (2021, 2022, 2023).
    Sortie : [annee,] departement, nb_stations, prix_median, q1, q3, iqr_cts, ecart_p90_p10_cts.
    """
    df = prix_hebdo.copy()
    df[COL_DEPARTEMENT] = df[COL_DEPARTEMENT].astype(str)

    cles = [COL_DEPARTEMENT]
    if par_annee:
        df["annee"] = pd.to_datetime(df["semaine"]).dt.year
        cles = ["annee", COL_DEPARTEMENT]

    par_station = (
        df.groupby([*cles, COL_STATION])
        .agg(prix_station=("prix_hebdo", "median"))
        .reset_index()
    )

    stats = (
        par_station.groupby(cles)["prix_station"]
        .agg(
            nb_stations="count",
            prix_median="median",
            q1=lambda s: s.quantile(0.25),
            q3=lambda s: s.quantile(0.75),
            p10=lambda s: s.quantile(0.10),
            p90=lambda s: s.quantile(0.90),
        )
        .reset_index()
    )

    stats["iqr_cts"] = ((stats["q3"] - stats["q1"]) * 100).round(2)
    stats["ecart_p90_p10_cts"] = ((stats["p90"] - stats["p10"]) * 100).round(2)
    stats[["prix_median", "q1", "q3"]] = stats[["prix_median", "q1", "q3"]].round(3)

    return stats[
        [
            *cles,
            "nb_stations",
            "prix_median",
            "q1",
            "q3",
            "iqr_cts",
            "ecart_p90_p10_cts",
        ]
    ]