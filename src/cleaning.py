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

    À appeler une année à la fois : l'échelle (ANO-06) et les bornes
    (ANO-05, ANO-07) sont calculées par année.

    Responsable : Samuel (#14).
    """
    # Nouvelle table aux noms du contrat D-11 ; la table brute reste intacte
    # pour pouvoir comparer avant/après dans le notebook
    historique = pd.DataFrame({
        "id_station": historique_brut["id_pdv"],
        "code_postal": historique_brut["cp"],
        "departement": historique_brut["departement"],
        "implantation": historique_brut["pop"],
        # Sans format précis, une date mal écrite passerait inaperçue : ici elle lève une erreur
        "date_releve": pd.to_datetime(historique_brut["date"], format="%Y-%m-%dT%H:%M:%S"),
        # float dès le départ : en 2021 les prix sont des entiers (1499), la division par 1000 donnerait une erreur
        "prix_gazole": pd.to_numeric(historique_brut["prix"], errors="coerce").astype(float),
    })

    # ANO-06 : en 2021 les prix sont en millièmes d'euro (ex. 1499 pour 1,499 €).
    # À faire avant les seuils, sinon tous les prix de 2021 passeraient en NaN
    annee_2021 = historique["date_releve"].dt.year == 2021
    historique.loc[annee_2021, "prix_gazole"] = historique.loc[annee_2021, "prix_gazole"] / 1000

    # ANO-04 : même station au même instant avec deux prix différents.
    # On garde la dernière ligne du fichier (hypothèse : c'est la saisie la plus récente)
    historique = historique.drop_duplicates(
        subset=["id_station", "date_releve"], keep="last"
    )

    # ANO-02 et ANO-03 : prix impossibles (< 1 € ou > 3 €, seuil métier) passés en NaN.
    # La ligne reste : on perd la valeur invalide, pas le relevé.
    # Les prix plausibles sont conservés ; les écarts à la station relèvent d'ANO-07.
    prix_impossible = (historique["prix_gazole"] < 1) | (historique["prix_gazole"] > 3)
    historique.loc[prix_impossible, "prix_gazole"] = float("nan")

    # ANO-05 : prix très inférieurs au prix habituel de la station (règle 1,5 x IQR, borne basse).
    # On ne touche pas à la borne haute : les prix élevés de 2023 sont réels (ANO-03).
    prix_valides = historique["prix_gazole"].dropna()
    q1 = prix_valides.quantile(0.25)
    q3 = prix_valides.quantile(0.75)
    borne_basse = q1 - 1.5 * (q3 - q1)
    prix_trop_bas = historique["prix_gazole"] < borne_basse
    historique.loc[prix_trop_bas, "prix_gazole"] = float("nan")

    # ANO-07 : prix très supérieurs au prix habituel de la station (> 1,5 x sa médiane).
    # Les NaN déjà posés sont ignorés par la médiane, d'où l'ordre : après ANO-02/03/05.
    mediane_station = historique.groupby("id_station")["prix_gazole"].transform("median")
    prix_trop_haut = historique["prix_gazole"] / mediane_station > 1.5
    historique.loc[prix_trop_haut, "prix_gazole"] = float("nan")

    return historique


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


def joindre_historique_stations(
    historique: pd.DataFrame, stations: pd.DataFrame
) -> pd.DataFrame:
    """Ajoute aux relevés la description des stations du flux v2 (EF-06).

    Jointure gauche : les relevés des stations absentes du flux sont gardés (ANO-13).
    Responsable : Noé (#35).
    """
    # Uniquement ce que l'historique n'a pas : code postal et implantation y sont
    # déjà, et ils valent à la date du relevé (une station a pu changer depuis)
    infos_flux = stations[["id_station", "departement", "ville", "latitude", "longitude"]]

    # Le département existe des deux côtés avec des valeurs différentes (ANO-12) :
    # on garde les deux pour choisir ensuite (D-18) au lieu d'en écraser un
    infos_flux = infos_flux.rename(columns={"departement": "departement_flux"})

    nb_releves_avant = len(historique)
    historique_joint = historique.merge(
        infos_flux, on="id_station", how="left", validate="many_to_one"
    )

    # Une jointure gauche sur une clé unique à droite ne doit ni ajouter ni perdre de relevé
    assert len(historique_joint) == nb_releves_avant, "la jointure a changé le nombre de relevés"

    # ----- AJOUT 3b -----
    # D-18 : le département officiel du flux fait foi (ANO-12). Pour les stations
    # absentes du flux (ANO-13), on garde celui tiré du code postal, seul disponible
    departement_officiel = historique_joint["departement_flux"].notna()
    historique_joint.loc[departement_officiel, "departement"] = historique_joint.loc[
        departement_officiel, "departement_flux"
    ]
    historique_joint = historique_joint.drop(columns="departement_flux")
    # ----- FIN AJOUT -----

    return historique_joint