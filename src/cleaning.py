"""Chargement et nettoyage des données de prix des carburants (contrat : D-11)."""

import gzip
import xml.etree.ElementTree as ET
import zipfile

import pandas as pd

# Liste partagée pour que tout le monde filtre le même périmètre (D-07)
DEPARTEMENTS_IDF = ["75", "77", "78", "91", "92", "93", "94", "95"]


def charger_historique(annee: int) -> pd.DataFrame:
    """Lit l'historique XML d'une année, gazole et Île-de-France uniquement.

    Responsable : Hafsa (#9).
    """

    chemin_zip = f"data/raw/historique_{annee}.zip"
    nom_xml = f"PrixCarburants_annuel_{annee}.xml"
    idf_tuple = tuple(DEPARTEMENTS_IDF)

    donnees = []

    # iterparse lit le gros fichier petit à petit directement depuis le zip
    with zipfile.ZipFile(chemin_zip) as archive, archive.open(nom_xml) as fichier:
        context = ET.iterparse(fichier, events=("end",))

        for event, elem in context:
            if elem.tag == "pdv":
                cp = elem.get("cp", "")

                # 1er Filtre : On vérifie si c'est en Île-de-France
                if cp.startswith(idf_tuple):
                    id_pdv = elem.get("id")
                    ville = elem.findtext("ville")

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
                                    "departement": cp[:2],
                                    "ville": ville,
                                    "pop": pop,
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


def lire_flux_v2(chemin: str = "data/raw/flux_v2.csv") -> pd.DataFrame:
    """Lit le flux v2 brut (toutes les stations), en clair ou compressé gzip.

    Responsable : Thikana (#22).
    """
    try:
        return pd.read_csv(
            chemin, sep=";", dtype=str, compression="gzip", encoding="utf-8-sig"
        )
    except gzip.BadGzipFile:
        return pd.read_csv(chemin, sep=";", dtype=str, encoding="utf-8-sig")


def charger_stations(chemin: str = "data/raw/flux_v2.csv") -> pd.DataFrame:
    """Lit le flux v2 (clair ou gzip), Île-de-France.

    Responsable : Thikana (#22).
    """
    stations_brutes = lire_flux_v2(chemin)

    stations_idf = stations_brutes[
        stations_brutes["code_departement"].isin(DEPARTEMENTS_IDF)
    ]

    colonnes_utiles = [
        "id",
        "Code postal",
        "Ville",
        "pop",
        "latitude",
        "longitude",
        "code_departement",
    ]

    return stations_idf[colonnes_utiles]


def nettoyer_stations(stations_brutes: pd.DataFrame) -> pd.DataFrame:
    """Applique les traitements des fiches ANO-10 et suivantes, format D-11.

    Responsable : Noé (#27).
    """
    # Nouvelle table aux noms du contrat D-11, identiques à l'historique pour la jointure EF-06.
    # La table brute n'est pas modifiée, ce qui permet de comparer avant/après dans le notebook
    stations = pd.DataFrame({
        "id_station": stations_brutes["id"],
        "code_postal": stations_brutes["Code postal"],
        # Département officiel, jamais les 2 premiers chiffres du code postal (ANO-12)
        "departement": stations_brutes["code_departement"],
        "ville": stations_brutes["Ville"],
        "implantation": stations_brutes["pop"],
        "latitude": stations_brutes["latitude"],
        "longitude": stations_brutes["longitude"],
    })

    # Les coordonnées sont stockées en degrés × 100 000 (ANO-11) :
    # on les remet en degrés pour les cartes et les distances
    stations["latitude"] = pd.to_numeric(stations["latitude"], errors="coerce") / 100000
    stations["longitude"] = pd.to_numeric(stations["longitude"], errors="coerce") / 100000

    # Garde-fous : le flux change à chaque téléchargement, on s'arrête si un cas
    # non prévu par les fiches ANO apparaît (une station décrite deux fois fausserait la jointure)
    assert stations["id_station"].duplicated().sum() == 0, "id de station en double"

    # Le flux ne doit contenir que R (route) et A (autoroute) ; voir ANO-14 pour l'historique
    implantation_connue = stations[stations["implantation"].isin(["R", "A"])]
    assert len(implantation_connue) == len(stations), "valeur de pop inconnue"

    # Un code postal de moins de 5 caractères a perdu son zéro initial
    code_postal_valide = stations[stations["code_postal"].str.len() == 5]
    assert len(code_postal_valide) == len(stations), "code postal mal formé"

    return stations
