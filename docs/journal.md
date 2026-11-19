# Journal de bord

_Mis à jour par le chef de projet au début de chaque semaine école et après chaque point à distance. 15 lignes maximum._

- **Semaine / jalon** : S47 · J3 Construction (16 → 20/11) · tag attendu : `v0.3`
- **Tags** : `v0.1` et `v0.2` posés le 16/11 en retard (D-14)
- **Prochaine échéance** : `v0.3` : statistiques consolidées, H-1 à H-3 testées, tableau de bord bêta ; puis PC3 (30/11 → 04/12)
- **Périmètre retenu** : Île-de-France, 2021-2023, gazole (D-06, D-07)
- **Questions analytiques** : v1 validée par le commanditaire le 28/10 (Q-05) ; hypothèses H-1 à H-3 formulées (#25)

**Rôles cette semaine**

**Rôles cette semaine**

| Membre             | GitHub          | Rôle (S47)              | Issues        |
| ------------------ | --------------- | ----------------------- | ------------- |
| Noé Chauvin        | @NoeChv-n       | Chef de projet (fixe)   | #44, #46, #47 |
| Thikana Mageswaran | @Thikana17      | Responsable données     | #41           |
| Samuel Sanvee      | @Samolo007      | Responsable dépôt       | #43, #45      |
| Hafsa Aboulfaid    | @aboulfaidhafsa | Responsable restitution | #42           |

**Fait** : flux v2 et historique 2023 explorés (#22, #21) ; premiers indicateurs (#23) ; nettoyage des stations (#27) ; ANO-02/03 et ANO-10 à 14 documentées
**En cours** : nettoyage de l'historique (#26) ; outil de tableau de bord (#24) ; jointure (#35)
**Bloquants** : #26 conditionne #35, les tests d'hypothèses et le tableau de bord ; dates de la remise 2022 à sourcer (H-3) ; D-03, D-12, D-13 à valider

---

## Entrées

_Les plus récentes en haut. Format produit par le LLM avec le mot « clôture ». On garde les ~15 dernières ; les plus anciennes sont déplacées dans `journal-archive.md` à chaque jalon._

> **À quoi sert ce fichier** : c'est la mémoire commune de l'équipe et de nos LLM. Chacun le lit en début de session et y ajoute une entrée en fin de session.
> **Ce qu'il ne remplace pas** : les décisions vont dans `decisions.md`, les anomalies dans `anomalies.md`, les questions au commanditaire dans `questions.md`. Ici on **renvoie** vers ces fichiers, on ne recopie pas.
> **Règles** : l'entrée de journal est commitée dans la même PR que le travail qu'elle décrit. En cas de conflit sur ce fichier, on garde les deux blocs.

### 2026-11-17 · Noé · Chef de projet · Issue #35
- **Fait** : `joindre_historique_stations()` écrite dans `src/cleaning.py` (jointure gauche, `validate="many_to_one"`, contrôle du nombre de relevés : 587 082 → 587 082) ; notebook `02_jointure` avec contrôles EF-06 et enregistrement de `historique_joint_idf.parquet`
- **Décisions** : D-18 département du flux retenu, code postal pour les stations absentes du flux (proposée) → déjà dans decisions.md, à valider en équipe
- **Anomalies** : ANO-12 complétée (4 stations, 802 relevés) ; ANO-13 recomptée (121 / 908 stations, 7,8 % des relevés), écart avec les 52 % expliqué
- **Bloquant / question** : aucun ; H-2 et `03_analyse` peuvent maintenant lire la table jointe
- **Prochaine étape** : ouvrir la PR `Closes #35` relue par Thikana, puis créer les issues H-1, H-2, H-3 et tableau de bord bêta

### 2026-11-17 · Samuel · Responsable dépôt · Issue #26
- **Fait** : fonction de nettoyage de l'historique 2021-2023 écrite dans src/cleaning.py, notebook 02_nettoyage_historique et Parquet de 587 082 lignes produits
- **Décisions** : D-16 (doublons, dernière ligne gardée) et D-17 (prix aberrants année par année) → déjà dans decisions.md
- **Anomalies** : ANO-02 à ANO-07 créées ou complétées, ANO-14 corrigée (1 station, 47 relevés en 2021)
- **Bloquant / question** : questions pour Hafsa à poster dans la PR ; échelle 2021 (ANO-06) non confirmée par la documentation du producteur ; D-16 et D-17 à valider
- **Prochaine étape** : ouvrir la PR avec Closes #26 et la faire relire par Thikana

### 2026-11-16 · Noé · Chef de projet · Issue #36
- **Fait** : tags `v0.1` (PR #18) et `v0.2` (PR #33) posés en retard ; « État actuel » du journal passé en S47 / J3 ; issue #35 (jointure EF-06) créée avec Thikana
- **Décisions** : D-14 pose tardive des tags (proposée) → déjà dans decisions.md, à valider en équipe
- **Anomalies** : aucune
- **Bloquant / question** : rôles S47 de Thikana, Samuel et Hafsa à confirmer ; #26 conditionne la jointure #35
- **Prochaine étape** : écrire `joindre_historique_stations()` dans `src/cleaning.py` (#35)

### 2026-11-16 · Noé · Chef de projet · Issue #27
- **Fait** : `nettoyer_stations()` écrite dans `src/cleaning.py` (colonnes D-11, coordonnées converties en degrés, contrôles doublons / pop / code postal) ; notebook `02_nettoyage_stations` avec bilan 833 → 833 lignes et Parquet `stations_idf` ; fiches ANO-10 à ANO-14, récapitulatif et contrôles 1 à 3 complétés
- **Décisions** : aucune (contrat D-11 appliqué tel quel)
- **Anomalies** : ANO-10, 11, 12 traitées ; ANO-13 et 14 renvoyées à la jointure et à `nettoyer_historique()` (#14)
- **Bloquant / question** : vérifier que `charger_historique()` présente dans la branche vient de `main` ; ruff signale I001, SIM117 et E501 hors de ma fonction (à transmettre à Hafsa et Thikana) ; station 94160001 hors du regroupement Paris de D-08
- **Prochaine étape** : ouvrir la PR `Closes #27` et créer l'issue de jointure citant ANO-12 et ANO-13

### 2026-11-16 · Noé · Chef de projet · Suivi PR #31

- **Fait** : tableau récapitulatif de anomalies.md aligné sur les fiches ANO-02/03 ; ampleur d'ANO-03 corrigée (631 = 3 + 628) ; entrée de journal du 16/11 replacée en haut ; README pointé vers 01_exploration_historique.ipynb ; cleaning.py formaté avec ruff
- **Décisions** : aucune nouvelle
- **Anomalies** : à créer dans #14 : prix 2021 en millièmes d'euro (1790 au lieu de 1.79)
- **Bloquant / question** : numérotation ANO-02 à 09 à trancher entre Hafsa et Samuel
- **Prochaine étape** : PR relue par Hafsa

### 2026-11-16 · Hafsa · Responsable données · Issue #21

- **Fait** : résolution des conflits Git sur `indicators.py`, nettoyage du code (`cleaning.py`) et du notebook, et correction de la documentation des anomalies suite à la review.
- **Décisions** : définition de seuils métier pour le nettoyage des prix (ANO-02 : < 1 € remplacés par NaN ; ANO-03 : > 3 € remplacés par NaN, maintien des pics réels à 2,19-2,62 €).
- **Anomalies** : mise à jour des fiches ANO-02 et ANO-03 avec les nouvelles règles métier.
- **Bloquant / question** : aucun
- **Prochaine étape** : pousser les corrections sur GitHub pour le merge final.

### 2026-11-15 · Noé · Chef de projet · Issue #25
- **Fait** : hypothèses H-1 à H-3 complétées dans questions.md (indicateur, méthode de comparaison descriptive, statut « Formulée ») ; énoncés inchangés depuis le 28/10, donc antérieurs aux premiers calculs de Samuel (#11)
- **Décisions** : aucune nouvelle ; pas de seuil chiffré ajouté à H-2, pour ne pas le fixer après avoir vu les médianes par département
- **Anomalies** : aucune
- **Bloquant / question** : dates et montants officiels de la remise 2022 à sourcer avant de tester H-3 (QA-4.3)
- **Prochaine étape** : faire valider H-1 à H-3 par l'équipe en commentaire de #25, puis démarrer #27 (nettoyage du flux des stations)

### 2026-11-10 · Samuel · Responsable restitution · Issue #11

- **Fait** : test de prix_hebdo_par_station, prix_median_hebdo et prix_median_par_departement sur les données brutes 2023 (IDF, gazole : 175 351 relevés, 831 stations)
- **Décisions** : traitement de la 1re semaine partielle (01/01/2023) et des semaines vides à proposer au chef → à reporter dans decisions.md
- **Anomalies** : aucune créée ; 25 prix hors 1 à 3 €/L, 831 stations sur 1 640, semaines vides à signaler à Hafsa sur l'issue #9
- **Bloquant / question** : sens d'une semaine sans relevé (donnée manquante ou prix inchangé) à vérifier dans la documentation du producteur ; notebooks/01_exploration.ipynb vide fait échouer ruff
- **Prochaine étape** : choix de l’outil de tableau de bord

### 2026-10-28 · Noé · Chef de projet · Issue #7

- **Fait** : issue reprise de Hafsa ; `src/download.py` écrit et testé (historiques 2021-2023 et flux v2 CSV dans `data/raw/`, lancement `python src/download.py`, ruff OK) ; section Données du README mise à jour (URL, date de téléchargement)
- **Décisions** : aucune nouvelle (flux v2 en CSV déjà tracé en D-10)
- **Anomalies** : ANO-01 créée (flux v2 servi tantôt compressé gzip, tantôt en clair)
- **Bloquant / question** : lecture du flux v2 à fournir avant son exploration (ANO-01) ; XML 2021 de 307 Mo décompressé, risque mémoire sur 8 Go à tester tôt (ET-05)
- **Prochaine étape** : faire relire la PR #7 par Thikana, puis créer l'issue de lecture et de nettoyage du flux v2

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

### 2026-11-09 · Thikana · Responsable dépôt · Issue #22

- **Fait** : charger_stations() et lire_flux_v2() (flux en clair ou gzip) dans src/cleaning.py ; notebook 01_exploration_stations.ipynb (profil EF-02, contrôles, 831 stations en IDF dont 38 d'autoroute) ; historique 2021 relu : 838 stations IDF sur 1 607 absentes du flux (≈ 52 %)
- **Décisions** : lecture du flux v2 en clair ou gzip dans une fonction dédiée ; ajout du dossier parent au chemin d'import pour appeler src depuis notebooks/ (hors cours) → à reporter dans decisions.md
- **Anomalies** : ANO-10 à ANO-14 créées (région manquante, coordonnées en degrés × 100 000, code postal incohérent, stations absentes du flux, pop = N dans l'historique)
- **Bloquant / question** : historique_2021.zip était incomplet et le flux v2 servi en gzip (ANO-01), 52 % d'absents en IDF à discuter pour la jointure EF-06
- **Prochaine étape** : pousser la branche et ouvrir la PR (Closes #22) avec un relecteur nommé


