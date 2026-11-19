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




# --- Axe QA-3 (Thikana) ---
VOLUME_REFERENCE_L = 100  # D-09 : volume de référence pour les écarts en euros

def ecart_autoroute_hebdo(prix_hebdo: pd.DataFrame) -> pd.DataFrame:
    """Écart hebdomadaire du prix du gazole, autoroute (A) moins route (R) (H-1).

    Entrée : sortie de prix_hebdo_par_station(). Responsable : Thikana.
    Sortie : semaine, mediane_a, mediane_r (€/L), nb_a, nb_r, ecart_cts, ecart_pct,
    ecart_euros_100l.
    """
    # La station dont l'implantation change selon l'année (N, A puis R) est exclue
    # en entier : son type de route n'est pas fiable (ANO-14 et fiche à venir)

    lignes_n = prix_hebdo[prix_hebdo[COL_IMPLANTATION] == "N"]
    stations_n = lignes_n[COL_STATION].unique()
    prix_ar = prix_hebdo[~prix_hebdo[COL_STATION].isin(stations_n)]

    # Les semaines sans prix ne comptent pas dans les effectifs (D-13).
    prix_ar = prix_ar.dropna(subset=["prix_hebdo"])

    medianes = prix_ar.pivot_table(
        index="semaine", columns=COL_IMPLANTATION, values="prix_hebdo", aggfunc="median"
    )
    effectifs = prix_ar.pivot_table(
        index="semaine", columns=COL_IMPLANTATION, values="prix_hebdo", aggfunc="count"
    )

    resultat = medianes.rename(columns={"A": "mediane_a", "R": "mediane_r"})
    resultat["nb_a"] = effectifs["A"]
    resultat["nb_r"] = effectifs["R"]

    # Prix en €/L : x 100 pour obtenir des cts/L ; le % est rapporté à la médiane R.
    resultat["ecart_cts"] = (resultat["mediane_a"] - resultat["mediane_r"]) * 100
    resultat["ecart_pct"] = resultat["ecart_cts"] / (resultat["mediane_r"] * 100) * 100

    # D-09 : écart en € pour 100 L de gazole (1 ct/L = 1 € pour 100 L).
    resultat["ecart_euros_100l"] = resultat["ecart_cts"] * VOLUME_REFERENCE_L / 100

    resultat.columns.name = None
    return resultat.reset_index()