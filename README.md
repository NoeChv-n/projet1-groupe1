# Prix des carburants : où et quand faire le plein au meilleur prix

Projet 1 DIA2 (UE01), HETIC, 2026-2027. Groupe 1.

## Contexte
Le commanditaire est une fédération régionale de transporteurs routiers (fictive), pour qui le carburant est le premier poste de dépense après les salaires.

Question posée : « Nous voulons savoir où et quand faire le plein coûte le moins cher, quel est le surcoût réel des autoroutes et comment les prix ont réagi aux chocs récents. »

Sujet retenu : **n° 10, Prix des carburants** (annexe A du CDC-DIA2-UE01-2026).

## Questions analytiques
Version v1 validée par le commanditaire le 28/10/2026 (détail et colonnes : [`docs/questions.md`](docs/questions.md)).

1. **Où** le gazole est-il le moins cher dans la région ?
2. **À quel moment** le plein coûte-t-il le moins cher ?
3. Quel est le **surcoût réel de l'autoroute** ?
4. **Comment le prix a-t-il évolué** sur la période ?

Toute modification ultérieure des questions est soumise par écrit au commanditaire et tracée ici.

## Données

- **Source** : data.gouv.fr, « Prix des carburants en France »
- **Producteur** : Ministère de l'Économie (ministères économiques et financiers)
- **Licence** : [Licence Ouverte Etalab 2.0](https://www.etalab.gouv.fr/licence-ouverte-open-licence)
- **URL** :
  - [Historique 2021](https://donnees.roulez-eco.fr/opendata/annee/2021)
  - [Historique 2022](https://donnees.roulez-eco.fr/opendata/annee/2022)
  - [Historique 2023](https://donnees.roulez-eco.fr/opendata/annee/2023)
  - Flux v2 (stations) : version CSV, [page du jeu de données](https://www.data.gouv.fr/datasets/prix-des-carburants-en-france-flux-instantane-v2-ameliore) (choix du format : D-10)
- **Date de téléchargement** : 2026-10-27
- **Dernière mise à jour des données (producteur)** : à compléter (issue #6)
- **Périmètre retenu** : Île-de-France, 2021 à 2023, gazole, validé par le commanditaire le 28/10/2026 (D-06, D-07, Q-06)

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