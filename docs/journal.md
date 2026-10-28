# Journal de bord — Projet 1 · Prix des carburants · Groupe 1

> **À quoi sert ce fichier** : c'est la mémoire commune de l'équipe et de nos LLM. Chacun le lit en début de session et y ajoute une entrée en fin de session.
> **Ce qu'il ne remplace pas** : les décisions vont dans `decisions.md`, les anomalies dans `anomalies.md`, les questions au commanditaire dans `questions.md`. Ici on **renvoie** vers ces fichiers, on ne recopie pas.
> **Règles** : l'entrée de journal est commitée dans la même PR que le travail qu'elle décrit. En cas de conflit sur ce fichier, on garde les deux blocs.

## État actuel

_Mis à jour par le chef de projet au début de chaque semaine école et après chaque point à distance. 15 lignes maximum._

- **Semaine / jalon** : S44 · J2 Exploration (26 → 30/10) · tag attendu : `v0.2` — **`v0.1` en retard (attendue S41), à poser en priorité**
- **Prochaine échéance** : tag `v0.1` (issues #1 à #5), puis PC2 (02 → 06/11) : nettoyage terminé, jointure réalisée, maquette papier du tableau de bord
- **Périmètre retenu** : région [À COMPLÉTER], années [À COMPLÉTER], carburants [À COMPLÉTER] (issue #6, décision D-xx à venir)
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

### 2026-10-28 · Hafsa · Responsable données · Issue #6

- **Fait** : intégration des justifications détaillées du périmètre (IDF, 2021-2023, gazole).
- **Décisions** : détails complets ajoutés dans decisions.md (D-07).
- **Anomalies** : aucune
- **Bloquant / question** : aucun
- **Prochaine étape** : pousser la branche sur GitHub puis calculer les effectifs de l'IDF avec Pandas.
