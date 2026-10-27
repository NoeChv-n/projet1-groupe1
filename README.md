# Prix des carburants : où et quand faire le plein au meilleur prix

Projet 1 DIA2 (UE01), HETIC, 2026-2027. Groupe 1.

## Contexte
Le commanditaire est une fédération régionale de transporteurs routiers (fictive), pour qui le carburant est le premier poste de dépense après les salaires.

Question posée : « Nous voulons savoir où et quand faire le plein coûte le moins cher, quel est le surcoût réel des autoroutes et comment les prix ont réagi aux chocs récents. »

Sujet retenu : **n° 10, Prix des carburants** (annexe A du CDC-DIA2-UE01-2026).

## Questions analytiques
1. À définir (issue #5, questions non validées)


## Données

- **Source** : data.gouv.fr, « Prix des carburants en France »
- **Producteur** : Ministère de l'Économie (ministères économiques et financiers)
- **Licence** : [Licence Ouverte Etalab 2.0](https://www.etalab.gouv.fr/licence-ouverte-open-licence)
- **URL** :
  - [Historique 2021](https://donnees.roulez-eco.fr/opendata/annee/2021)
  - [Historique 2022](https://donnees.roulez-eco.fr/opendata/annee/2022)
  - [Historique 2023](https://donnees.roulez-eco.fr/opendata/annee/2023)
  - Flux v2 (stations) : [page du jeu de données](https://www.data.gouv.fr/datasets/prix-des-carburants-en-france-flux-instantane-v2-ameliore) (format du fichier à confirmer, issue #6) :
- **Date de téléchargement** : 2026-10-27
- **Périmètre retenu** (provisoire, voir `docs/decisions.md`) : Île-de-France, 2021 à 2023, gazole

## Installation
À compléter une fois `requirements.txt` créé.


## Reproduire l'analyse
1. Télécharger les données : `python src/download.py` (à confirmer)
2. Exécuter `notebooks/01_exploration.ipynb`
3. Lancer le tableau de bord : `streamlit run app/dashboard.py` (à confirmer)

## Résultats principaux
À compléter en fin de projet (3 à 5 constats).

## Limites
À compléter au fil de l'analyse.

## Équipe

| Membre | GitHub | Rôle (S44) |
|---|---|---|
| Noé Chauvin | @NoeChv-n | Chef de projet (fixe) |
| Thikana Mageswaran | @Thikana17 | Responsable dépôt (relectures, tag v0.1) |
| Samuel Sanvee | @Samolo007 | Responsable restitution |
| Hafsa Aboulfaid | @aboulfaidhafsa | Responsable données |