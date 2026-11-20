"""Calcul des indicateurs de prix (entrées au format D-11)."""

import pandas as pd

COL_STATION = "id_station"
COL_DEPARTEMENT = "departement"
COL_IMPLANTATION = "implantation"
COL_DATE = "date_releve"
COL_PRIX = "prix_gazole"
JOURS_SEMAINE = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


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


def ecart_mensuel_a_l_annee(historique: pd.DataFrame) -> pd.DataFrame:
    """Écart du prix médian de chaque mois au prix médian de son année (QA-2.1, H-4).

    Entrée : historique joint (D-11). Responsable : Noé (#44).
    Sortie : annee, mois, prix_median_mois, prix_median_annee, nb_stations,
    ecart_cts, ecart_pct, ecart_euros_100l.
    """
    historique = historique.copy()
    historique[COL_DATE] = pd.to_datetime(historique[COL_DATE])
    historique["annee"] = historique[COL_DATE].dt.year
    historique["mois"] = historique[COL_DATE].dt.month

    # Une station qui publie tous les jours ne doit pas peser plus qu'une autre
    prix_station_mois = historique.groupby([COL_STATION, "annee", "mois"]).agg(
        prix_mensuel=(COL_PRIX, "mean")
    )
    prix_station_mois = prix_station_mois.reset_index()

    # Référence de l'année sur la même base que les mois (une valeur par station et par mois)
    prix_station_mois["prix_median_annee"] = prix_station_mois.groupby("annee")[
        "prix_mensuel"
    ].transform("median")

    par_mois = prix_station_mois.groupby(["annee", "mois"]).agg(
        prix_median_mois=("prix_mensuel", "median"),
        prix_median_annee=("prix_median_annee", "first"),
        nb_stations=(COL_STATION, "nunique"),
    )
    par_mois = par_mois.reset_index()

    ecart = par_mois["prix_median_mois"] - par_mois["prix_median_annee"]
    par_mois["ecart_cts"] = (ecart * 100).round(2)
    par_mois["ecart_pct"] = (ecart / par_mois["prix_median_annee"] * 100).round(2)
    # D-09 : avec 100 L de référence, 1 ct/L d'écart vaut 1 €
    par_mois["ecart_euros_100l"] = par_mois["ecart_cts"]
    return par_mois

def comparer_profils_mensuels(ecarts_mensuels: pd.DataFrame) -> pd.DataFrame:
    """Écarts mensuels en cts/L, une colonne par année (QA-2.2, H-4).

    Entrée : sortie de ecart_mensuel_a_l_annee(). Responsable : Noé (#44).
    Sortie : mois, une colonne par année, nb_annees_au_dessus.
    """
    # Une seule valeur par mois et par année : la moyenne par défaut la recopie telle quelle
    profils = ecarts_mensuels.pivot_table(
        index="mois", columns="annee", values="ecart_cts"
    )

    # H-4 : un mois « cher » chaque année doit être au-dessus de sa médiane 3 fois sur 3
    profils["nb_annees_au_dessus"] = (profils > 0).sum(axis=1)

    # Le nom "annee" resterait collé à l'en-tête des colonnes après reset_index
    profils.columns.name = None
    return profils.reset_index()



def releves_par_jour_semaine(historique: pd.DataFrame) -> pd.DataFrame:
    """Nombre et part des relevés publiés chaque jour de la semaine (QA-2.3, diagnostic).

    Entrée : historique joint (D-11). Responsable : Noé (#44).
    Sortie : jour, nb_releves, part_releves_pct, nb_stations.
    """
    historique = historique.copy()
    historique[COL_DATE] = pd.to_datetime(historique[COL_DATE])
    # dt.dayofweek donne 0 pour lundi et 6 pour dimanche : on garde l'ordre de la semaine
    historique["num_jour"] = historique[COL_DATE].dt.dayofweek

    par_jour = historique.groupby("num_jour").agg(
        nb_releves=(COL_PRIX, "count"),
        nb_stations=(COL_STATION, "nunique"),
    )
    par_jour = par_jour.reset_index()

    par_jour["jour"] = [JOURS_SEMAINE[num] for num in par_jour["num_jour"]]
    # Si les stations publiaient au hasard, chaque jour aurait environ 14,3 % des relevés
    part = par_jour["nb_releves"] / par_jour["nb_releves"].sum() * 100
    par_jour["part_releves_pct"] = part.round(1)
    return par_jour[["jour", "nb_releves", "part_releves_pct", "nb_stations"]]

def ecart_par_jour_semaine(
    historique: pd.DataFrame, jours_max_sans_releve: int = 7
) -> pd.DataFrame:
    """Écart du prix médian de chaque jour de la semaine au prix médian global (QA-2.3).

    Entrée : historique joint (D-11). Responsable : Noé (#44).
    D-20 : entre deux relevés, le prix est supposé inchangé, au plus
    jours_max_sans_releve jours. Sortie : jour, prix_median, nb_station_jours, ecart_cts.
    """
    historique = historique.copy()
    historique[COL_DATE] = pd.to_datetime(historique[COL_DATE])

    # Un prix par station et par jour : le dernier publié, celui en vigueur le soir
    prix_jour = (
        historique.set_index(COL_DATE).groupby(COL_STATION)[COL_PRIX].resample("D").last()
    )
    # Un jour sans relevé reprend le dernier prix de la même station, 7 jours au plus (D-20)
    prix_jour = prix_jour.groupby(level=COL_STATION).ffill(limit=jours_max_sans_releve)
    prix_jour = prix_jour.dropna().reset_index()

    prix_jour["num_jour"] = prix_jour[COL_DATE].dt.dayofweek
    par_jour = prix_jour.groupby("num_jour").agg(
        prix_median=(COL_PRIX, "median"),
        nb_station_jours=(COL_PRIX, "count"),
    )
    par_jour = par_jour.reset_index()
    par_jour["jour"] = [JOURS_SEMAINE[num] for num in par_jour["num_jour"]]

    # Chaque jour revient autant de fois sur la période : la hausse générale pèse pareil sur tous
    ecart = par_jour["prix_median"] - prix_jour[COL_PRIX].median()
    par_jour["ecart_cts"] = (ecart * 100).round(2)
    return par_jour[["jour", "prix_median", "nb_station_jours", "ecart_cts"]]


VOLUME_REFERENCE_L = 100  # D-09 : volume de référence pour les écarts en euros

def exclure_stations_n(prix_hebdo: pd.DataFrame) -> pd.DataFrame:
    """Retire en entier les stations dont l'implantation vaut N (ANO-14)."""
    lignes_n = prix_hebdo[prix_hebdo[COL_IMPLANTATION] == "N"]
    stations_n = lignes_n[COL_STATION].unique()
    return prix_hebdo[~prix_hebdo[COL_STATION].isin(stations_n)]


def ecart_autoroute_hebdo(prix_hebdo: pd.DataFrame) -> pd.DataFrame:
    """Écart hebdomadaire du prix du gazole, autoroute (A) moins route (R) (H-1).

    Entrée : sortie de prix_hebdo_par_station(). Responsable : Thikana.
    Sortie : semaine, mediane_a, mediane_r (€/L), nb_a, nb_r, ecart_cts, ecart_pct,
    ecart_euros_100l.
    """
    # La station dont l'implantation change selon l'année (N, A puis R) est exclue
    # en entier : son type de route n'est pas fiable (ANO-14 et ANO-15).

    prix_ar = exclure_stations_n(prix_hebdo)

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


def ecart_autoroute_par_periode(
    ecart_hebdo: pd.DataFrame, periode: str = "trimestre"
) -> pd.DataFrame:
    """Médiane de l'écart autoroute - route par trimestre ou par année (QA-3.2).

    Entrée : sortie de ecart_autoroute_hebdo(). Responsable : Thikana.
    periode : "trimestre" ou "annee". Sortie : une ligne par période, avec
    ecart_cts, ecart_pct, ecart_euros_100l (médianes) et nb_a_median, nb_a_min.
    """
    ecart_hebdo = ecart_hebdo.copy()
    ecart_hebdo["annee"] = ecart_hebdo["semaine"].dt.year
    ecart_hebdo["trimestre"] = ecart_hebdo["semaine"].dt.quarter

    if periode == "annee":
        cles = ["annee"]
    elif periode == "trimestre":
        cles = ["annee", "trimestre"]
    else:
        raise ValueError('periode doit valoir "annee" ou "trimestre"')

    par_periode = ecart_hebdo.groupby(cles).agg(
        ecart_cts=("ecart_cts", "median"),
        ecart_pct=("ecart_pct", "median"),
        ecart_euros_100l=("ecart_euros_100l", "median"),
        nb_a_median=("nb_a", "median"),
        nb_a_min=("nb_a", "min"),
        nb_semaines=("semaine", "count"),
    )
    return par_periode.reset_index()


def ecart_autoroute_par_departement(
    prix_hebdo: pd.DataFrame, seuil_stations_a: int = 5
) -> pd.DataFrame:
    """Écart autoroute - route à département égal (QA-3.3, EF-08).

    Entrée : sortie de prix_hebdo_par_station(). Responsable : Thikana.
    interprete vaut True si le département compte au moins seuil_stations_a
    stations A (D-19). Sortie : une ligne par département ayant des stations A.
    """
    prix_ar = exclure_stations_n(prix_hebdo)
    stations = prix_ar.drop_duplicates(subset=COL_STATION)

    resultats = []
    for departement in stations[COL_DEPARTEMENT].unique():
        stations_dep = stations[stations[COL_DEPARTEMENT] == departement]
        nb_stations_a = (stations_dep[COL_IMPLANTATION] == "A").sum()
        if nb_stations_a == 0:
            continue  # pas de comparaison possible (ex. Paris)

<<<<<<< HEAD
        prix_dep = prix_ar[prix_ar[COL_DEPARTEMENT] == departement]
        ecart = ecart_autoroute_hebdo(prix_dep)
        resultats.append(
            {
                "departement": departement,
                "nb_stations_a": nb_stations_a,
                "nb_stations_r": (stations_dep[COL_IMPLANTATION] == "R").sum(),
                "ecart_cts": ecart["ecart_cts"].median(),
                "ecart_pct": ecart["ecart_pct"].median(),
                "ecart_euros_100l": ecart["ecart_euros_100l"].median(),
                "semaines_positives": (ecart["ecart_cts"] > 0).sum(),
                "nb_semaines": ecart["ecart_cts"].notna().sum(),
                "interprete": nb_stations_a >= seuil_stations_a,
            }
        )
    return pd.DataFrame(resultats)
=======
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
    Pour le 75, les stations sans commune renseignée sont rattachées à "Paris".
    Sortie : departement, ville, prix_median (€/L), nb_stations,
    ecart_med_reg_cts, ecart_med_reg_eur_100l, trié par prix croissant.
    """
    prix_hebdo = prix_hebdo_par_station(historique_joint)

    villes = (
        historique_joint[[COL_STATION, COL_DEPARTEMENT, "ville"]]
        .drop_duplicates(subset=[COL_STATION], keep="last")
        .copy()
    )
    masque_paris = (villes[COL_DEPARTEMENT].astype(str) == "75") & (
        villes["ville"].isna()
    )
    villes.loc[masque_paris, "ville"] = "Paris"
    villes = villes[[COL_STATION, "ville"]].dropna(subset=["ville"])

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
    prix_hebdo: pd.DataFrame, par_annee: bool = True
) -> pd.DataFrame:
    """Dispersion intra-départementale des prix médians par station (QA-1.3).

    Entrée : sortie de prix_hebdo_par_station() issue de la table jointe (D-18 appliquée).
    Si par_annee=True (défaut), le calcul est effectué année par année (2021, 2022, 2023).
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

