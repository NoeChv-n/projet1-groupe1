"""Chargement et nettoyage des données de prix des carburants (contrat : D-11)."""

import pandas as pd
import xml.etree.ElementTree as ET
# Liste partagée pour que tout le monde filtre le même périmètre (D-07)
DEPARTEMENTS_IDF = ["75", "77", "78", "91", "92", "93", "94", "95"]


def charger_historique(annee: int) -> pd.DataFrame:
    """Lit l'historique XML d'une année, gazole et Île-de-France uniquement.

    Responsable : Hafsa (#9).
    """
    chemin = f"data/raw/PrixCarburants_annuel_{annee}.xml"
    idf_tuple = tuple(DEPARTEMENTS_IDF)
    
    donnees = []
    
    # iterparse lit le gros fichier petit à petit pour ne pas faire exploser la RAM
    context = ET.iterparse(chemin, events=("end",))
    
    for event, elem in context:
        if elem.tag == "pdv":
            cp = elem.get("cp", "")
            
            # 1er Filtre : On vérifie si c'est en Île-de-France
            if cp.startswith(idf_tuple):
                id_pdv = elem.get("id")
                ville = elem.findtext("ville")
                
                # On parcourt les sous-balises prix de cette station
                for prix in elem.findall("prix"):
                    nom_carburant = prix.get("nom")
                    
                    # 2ème Filtre (D-06 / D-07) : Uniquement le Gazole
                    if nom_carburant == "Gazole":
                        donnees.append({
                            "id_pdv": id_pdv,
                            "cp": cp.zfill(5),
                            "ville": ville,
                            "carburant": nom_carburant,
                            "date": prix.get("maj"),
                            "prix": prix.get("valeur")
                        })
            
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
