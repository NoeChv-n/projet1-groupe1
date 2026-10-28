"""Chargement et nettoyage des données de prix des carburants (contrat : D-11)."""

import pandas as pd

# Liste partagée pour que tout le monde filtre le même périmètre (D-07)
DEPARTEMENTS_IDF = ["75", "77", "78", "91", "92", "93", "94", "95"]


def charger_historique(annee: int) -> pd.DataFrame:
    """Lit l'historique XML d'une année, gazole et Île-de-France uniquement.

    Responsable : Hafsa (#9).
    """


def nettoyer_historique(historique_brut: pd.DataFrame) -> pd.DataFrame:
    """Applique les traitements des fiches ANO-01 à 09, renvoie le format D-11.

    Responsable : Samuel (#14).
    """


def charger_stations(chemin: str = "data/raw/stations_flux_v2.csv") -> pd.DataFrame:
    """Lit le flux v2 (.csv ou .csv.gz, compression détectée), Île-de-France.

    Responsable : Thikana (#10).
    """


def nettoyer_stations(stations_brutes: pd.DataFrame) -> pd.DataFrame:
    """Applique les traitements des fiches ANO-10 et suivantes, format D-11.

    Responsable : Noé (#15).
    """
