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
    """
    historique = historique.copy()
    historique[COL_DATE] = pd.to_datetime(historique[COL_DATE])

    par_station = historique.set_index(COL_DATE).groupby(
        [COL_STATION, COL_DEPARTEMENT, COL_IMPLANTATION]
    )
    prix_hebdo = par_station[COL_PRIX].resample("W").mean()
    prix_hebdo = prix_hebdo.reset_index()
    prix_hebdo = prix_hebdo.rename(
        columns={COL_DATE: "semaine", COL_PRIX: "prix_hebdo"}
    )
    return prix_hebdo


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
    return par_departement.round(2)
