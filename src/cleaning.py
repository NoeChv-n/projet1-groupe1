"""Chargement et nettoyage des données de prix des carburants (contrat : D-11)."""

import xml.etree.ElementTree as ET
import zipfile  # Ajout de l'import pour lire les fichiers .zip

import pandas as pd

# Liste partagée pour que tout le monde filtre le même périmètre (D-07)
DEPARTEMENTS_IDF = ["75", "77", "78", "91", "92", "93", "94", "95"]


def charger_historique(annee: int) -> pd.DataFrame:
    """Lit l'historique XML d'une année, gazole et Île-de-France uniquement.

    Responsable : Hafsa (#9).
    """
    # Modification : Chemins pour lire depuis le fichier zip téléchargé
    chemin_zip = f"data/raw/historique_{annee}.zip"
    nom_xml = f"PrixCarburants_annuel_{annee}.xml"
    idf_tuple = tuple(DEPARTEMENTS_IDF)

    donnees = []

    # iterparse lit le gros fichier petit à petit directement depuis le zip
    with zipfile.ZipFile(chemin_zip) as archive:
        with archive.open(nom_xml) as fichier:
            context = ET.iterparse(fichier, events=("end",))

            for event, elem in context:
                if elem.tag == "pdv":
                    cp = elem.get("cp", "")

                    # 1er Filtre : On vérifie si c'est en Île-de-France
                    if cp.startswith(idf_tuple):
                        id_pdv = elem.get("id")
                        ville = elem.findtext("ville")
                        # Ajout de l'attribut pop demandé pour la colonne implantation (PR #30)
                        pop = elem.get("pop")

                        # On parcourt les sous-balises prix de cette station
                        for prix in elem.findall("prix"):
                            nom_carburant = prix.get("nom")

                            # 2ème Filtre (D-06 / D-07) : Uniquement le Gazole
                            if nom_carburant == "Gazole":
                                donnees.append(
                                    {
                                        "id_pdv": id_pdv,
                                        "cp": cp.zfill(5),
                                        "departement": cp[
                                            :2
                                        ],  # Ajout de la colonne département
                                        "ville": ville,
                                        "pop": pop,  # Ajout de la colonne pop
                                        # La ligne "carburant" a été retirée comme demandé
                                        "date": prix.get("maj"),
                                        "prix": prix.get("valeur"),
                                    }
                                )

                    # Très important : on efface l'élément de la mémoire après l'avoir lu
                    elem.clear()

    # On transforme notre liste en DataFrame Pandas
    df_idf = pd.DataFrame(donnees)

    return df_idf


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
