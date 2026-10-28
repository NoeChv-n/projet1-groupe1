"""Télécharge les données sources du projet (prix des carburants, licence Etalab 2.0).

Lancement depuis la racine du dépôt : python src/download.py
"""
import urllib.error
import urllib.request

DOSSIER_BRUT = "data/raw"
ANNEES = [2021, 2022, 2023]  # périmètre D-07

URL_HISTORIQUE = "https://donnees.roulez-eco.fr/opendata/annee/"  # + année
URL_FLUX_V2 = "https://www.data.gouv.fr/api/1/datasets/r/edd67f5b-46d0-4663-9de9-e5db1c880160"


def telecharger_fichier(url: str, chemin_destination: str) -> bool:
    """Télécharge `url` dans `chemin_destination`. Renvoie True si le téléchargement a réussi."""
    print(f"Téléchargement de {url} ...")
    try:
        urllib.request.urlretrieve(url, chemin_destination)
    except urllib.error.URLError as erreur:
        # On affiche la cause sans arrêter les autres téléchargements
        print(f"  ÉCHEC : {erreur}")
        return False
    print(f"  -> enregistré dans {chemin_destination}")
    return True


def telecharger_tout() -> None:
    """Télécharge l'historique des années retenues et le flux v2 dans data/raw/."""
    nb_echecs = 0
    for annee in ANNEES:
        if not telecharger_fichier(f"{URL_HISTORIQUE}{annee}", f"{DOSSIER_BRUT}/historique_{annee}.zip"):
            nb_echecs += 1
    # Le serveur renvoie ce fichier tantôt compressé (gzip), tantôt en clair (ANO-01) :
    # on l'enregistre tel quel, la lecture gère les deux cas
    if not telecharger_fichier(URL_FLUX_V2, f"{DOSSIER_BRUT}/flux_v2.csv"):
        nb_echecs += 1
    print(f"Terminé : {nb_echecs} échec(s).")

# Ce bloc ne s'exécute que si on lance le fichier directement (python src/download.py),
# pas quand le notebook ou le tableau de bord importent ses fonctions
if __name__ == "__main__":
    telecharger_tout()