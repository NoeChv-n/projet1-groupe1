# Journal de bord

*Mis à jour par le chef de projet au début de chaque semaine école et après chaque point à distance. 15 lignes maximum.*

- **Semaine / jalon** : S44 · J2 Exploration (26 → 30/10) · tag attendu : `v0.2` — **`v0.1` en retard (attendue S41), à poser en priorité**
- **Prochaine échéance** : tag `v0.1` (issues #1 à #5), puis PC2 (02 → 06/11) : nettoyage terminé, jointure réalisée, maquette papier du tableau de bord
- **Périmètre retenu** : région Ile de france, années 2021-2023, carburants gazole
- **Questions analytiques** : en cours de rédaction (issue #5), non validées

**Rôles cette semaine**

| Membre             | GitHub          | Rôle (S44)                               | Issues |
| ------------------ | --------------- | ---------------------------------------- | ------ |
| Noé Chauvin        | @NoeChv-n       | Chef de projet (fixe)                    | #3, #5 |
| Thikana Mageswaran | @Thikana17      | Responsable dépôt (relectures, tag v0.1) | #1, #2 |
| Samuel Sanvee      | @Samolo007      | Responsable restitution                  | #4     |
| Hafsa Aboulfaid    | @aboulfaidhafsa | Responsable données                      | #6, #7 |

**Fait** : dépôt `projet1-groupe1` créé et `main` protégée (D-02, D-03) ; issues #1 à #7 et milestones v0.1 / v0.2 ; documents de pilotage rédigés (#3, PR ouverte)
**En cours** : #1 structure du dépôt (Thikana) ; relecture PR #3 (Thikana) ; #5 questions analytiques (Noé)
**Bloquants** : aucun — D-03 à valider en équipe ; dates de Q-01 à compléter ; #1 conditionne #2, #4 et #7

---

## Entrées

_Les plus récentes en haut. Format produit par le LLM avec le mot « clôture ». On garde les ~15 dernières ; les plus anciennes sont déplacées dans `journal-archive.md` à chaque jalon._

> **À quoi sert ce fichier** : c'est la mémoire commune de l'équipe et de nos LLM. Chacun le lit en début de session et y ajoute une entrée en fin de session.
> **Ce qu'il ne remplace pas** : les décisions vont dans `decisions.md`, les anomalies dans `anomalies.md`, les questions au commanditaire dans `questions.md`. Ici on **renvoie** vers ces fichiers, on ne recopie pas.
> **Règles** : l'entrée de journal est commitée dans la même PR que le travail qu'elle décrit. En cas de conflit sur ce fichier, on garde les deux blocs.

### 2026-10-28 · Noé · Chef de projet · Issue #20
- **Fait** : squelette de `src/cleaning.py` et `src/indicators.py` (signatures, docstrings, ruff OK) ; plages ANO réservées par source dans anomalies.md
- **Décisions** : D-11 contrat de données, D-12 organisation des notebooks, précision de D-10 (`.csv` / `.csv.gz`) → déjà dans decisions.md, à valider en relecture
- **Anomalies** : aucune
- **Bloquant / question** : numéros d'issues GitHub différents de ceux du brief, à corriger ; propriétaire de `03_analyse` à désigner en J3 ; README « Reproduire » à mettre à jour par Samuel
- **Prochaine étape** : faire relire et fusionner la PR #20 par Thikana, puis donner le feu vert à l'équipe

### 2026-10-28 · Noé · Chef de projet · Issue #17
- **Fait** : retours du commanditaire archivés (Q-05 validation du cadrage v1, Q-06 format du flux v2) ; questions mises à jour (statuts, seuil QA-1.2, effectifs QA-3, sources QA-4.3) et hypothèses H-1 à H-3 formulées avant calcul ; merge de `main` avec résolution des conflits sur decisions.md et journal.md
- **Décisions** : D-08 seuil de 5 stations par commune, D-09 écarts en € pour 100 L, D-10 flux v2 en CSV (toutes proposées) → déjà dans decisions.md, à valider en équipe
- **Anomalies** : aucune créée — contrôle n° 5 complété (remise 2022, H-3)
- **Bloquant / question** : D-07 contient des résidus `[cite: …]` et un statut à mettre à jour (Q-06), à signaler à Hafsa
- **Prochaine étape** : pousser la branche et ouvrir la PR `Closes #17`, relue par Thikana

### 2026-10-27 · Samuel · Responsable restitution · Issue #4
- **Fait** : README complété selon l'annexe B (8 sections dans l'ordre) ; contexte, données et équipe rédigés, autres sections en « à compléter »
- **Décisions** : aucune
- **Anomalies** : aucune
- **Bloquant / question** : format du flux v2, date de téléchargement, dernière mise à jour des données et périmètre à confirmer avec Hafsa (#6) ; questions analytiques en attente (#5)
- **Prochaine étape** : faire relire la PR par Thikana
### 2026-10-27 · Noé · Chef de projet · Issue #5

- **Fait** : questions analytiques v1 rédigées (question principale + QA-1 à QA-4, 3 sous-questions chacune, reliées aux colonnes XML) ; exploration rapide du flux v2 et de l'historique 2025 (structure, volumes, stations autoroute par région) ; brouillons postés sur #5 et #6
- **Décisions** : D-05 rural/urbain écarté (proposée) ; D-06 gazole (validée commanditaire) → déjà dans decisions.md
- **Anomalies** : aucune créée — à documenter en exploration : `pop="N"` (1 station en 2025), relevés irréguliers par station
- **Bloquant / question** : Q-04 (chocs à analyser) en attente du commanditaire ; région et années à trancher dans #6
- **Prochaine étape** : intégrer les avis de l'équipe après la date limite, puis passer la PR #5 en « Ready for review »

### 2026-10-27 · Thikana · Responsable dépôt · Issue #1

- **Fait** : arborescence de l'annexe B créée, `.gitignore` écrit (données, .venv, pycache, checkpoints)
- **Décisions** : ajout de `docs/journal.md`, absent de l'annexe B → à reporter dans decisions.md
- **Anomalies** : aucune
- **Bloquant / question** : `.gitkeep` de `data/raw` et `data/processed` pas encore confirmés versionnés (`git ls-files data` vide)
- **Prochaine étape** : commiter les `.gitkeep`, pousser la branche et ouvrir la PR avec `Closes #1`

### 2026-10-27 · Noé · Chef de projet · Issue #3

- **Fait** : dépôt public créé, collaborateurs invités, `main` protégée ; issues #1 à #7 créées et assignées avec milestones ; documents de pilotage rédigés dans `docs/` et PR ouverte
- **Décisions** : D-02 (premier commit direct), D-03 (règle de relecture, à valider), D-04 (usage encadré du LLM) → déjà dans decisions.md
- **Anomalies** : aucune
- **Prochaine étape** : faire relire la PR #3 par Thikana, puis lancer la discussion de l'issue #5

### 2026-10-27 · Noé · Chef de projet · Issue #3

- **Fait** : mise en place des instructions LLM communes et du journal de bord
- **Décisions** : le dépôt GitHub est la source de vérité unique pour l'équipe et les LLM → reporté dans decisions.md (D-01)
- **Anomalies** : aucune
- **Bloquant / question** : aucun
- **Prochaine étape** : chaque membre configure son projet Claude / Gem et fait une première session test


### 2026-10-28 · Thikana · Responsable dépôt · Issue #2
- **Fait** : Configuration de l'environnement virtuel et création du `requirements.txt` avec les 8 dépendances directes figées pour assurer la compatibilité multi-OS (ET-01).
- **Décisions** : aucune
- **Anomalies** : aucune
- **Bloquant / question** : aucun
- **Prochaine étape** : Attendre l'approbation de la relecture pour fusionner la PR dans `main`.
### 2026-10-28 · Hafsa · Responsable données · Issue #6

- **Fait** : intégration des justifications détaillées du périmètre (IDF, 2021-2023, gazole).
- **Décisions** : détails complets ajoutés dans decisions.md (D-07).
- **Anomalies** : aucune
- **Bloquant / question** : aucun
- **Prochaine étape** : pousser la branche sur GitHub puis calculer les effectifs de l'IDF avec Pandas.
- **Prochaine étape** : chaque membre configure son projet Claude / Gem et fait une première session test
