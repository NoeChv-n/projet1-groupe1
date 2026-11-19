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
    # en entier : son type de route n'est pas fiable (ANO-14 et fiche à venir)

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