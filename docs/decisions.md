# Journal des décisions — Groupe 1

> Toute décision structurante (méthode, exclusion de données, périmètre, organisation) est notée ici **avant** ou **au moment** où elle s'applique.
> Une décision n'est jamais effacée : si elle change, on ajoute une nouvelle fiche qui indique « remplace D-xx ».

| Champ | Contenu attendu |
|---|---|
| Date | AAAA-MM-JJ |
| Décision | Ce qui est décidé, en une phrase |
| Justification | Pourquoi, avec renvoi au CDC si possible |
| Alternatives écartées | Ce qu'on n'a pas retenu et pourquoi |
| Statut | Proposée / Validée (par qui) / Remplacée par D-xx |

---

## D-01 · Le dépôt GitHub est la source de vérité unique
- **Date** : 2026-10-27
- **Décision** : l'équipe et les LLM s'appuient uniquement sur les fichiers du dépôt (journal, décisions, anomalies, questions, instructions).
- **Justification** : 4 membres, 2 outils LLM différents (Claude, Gemini) ; un seul endroit évite les versions divergentes. Cohérent avec L1 (reproductibilité).
- **Alternatives écartées** : documents partagés hors dépôt (pas d'historique, pas de relecture).
- **Statut** : Validée (équipe, 2026-10-27)

## D-02 · Premier commit poussé directement sur `main`
- **Date** : 2026-10-27
- **Décision** : le README initial a été poussé sur `main` avant l'activation de la protection de branche ; c'est la seule exception.
- **Justification** : une branche ne peut pas être protégée ni servir de base à une PR tant qu'elle ne contient aucun commit. Le sujet devait figurer dès le premier commit (CDC §4.3).
- **Alternatives écartées** : initialiser le dépôt avec le README généré par GitHub (titre seul, sujet absent).
- **Statut** : Validée (Noé)

## D-03 · Règle de relecture des pull requests
- **Date** : 2026-10-27
- **Décision** : le responsable dépôt de la semaine relit par défaut ; si il ou elle est indisponible ou auteur de la PR, n'importe quel autre membre relit. Personne ne relit sa propre PR.
- **Justification** : GIT-02 (1 approbation minimum) sans goulot d'étranglement ; rôle du responsable dépôt (CDC §11).
- **Alternatives écartées** : un relecteur unique fixe (bloque l'équipe en cas d'absence).
- **Statut** : Validée en équipe le 2026-11-19 (commentaire sur #47)

## D-04 · Usage encadré d'un LLM comme assistant pédagogique
- **Date** : 2026-10-27
- **Décision** : chaque membre utilise un LLM (Claude ou Gemini) configuré avec les instructions communes ; le LLM explique et propose, l'étudiant écrit, exécute et commite lui-même.
- **Justification** : accord du commanditaire sous réserves (voir questions.md, Q-01) ; la note se joue en revue de code individuelle.
- **Alternatives écartées** : usage libre sans cadre commun (code non maîtrisé, styles incohérents).
- **Statut** : Validée (commanditaire)

## D-05 · Comparaison rural / urbain écartée
- **Date** : 2026-10-27
- **Décision** : QA-1 compare les départements et les communes ; la distinction rural / urbain n'est pas traitée.
- **Justification** : les données ne contiennent pas cette information ; il faudrait une source externe (grille de densité INSEE), soumise à accord écrit du commanditaire (CDC §3). Charge jugée trop lourde pour une première prestation.
- **Alternatives écartées** : grille de densité INSEE (source supplémentaire, jointure en plus).
- **Statut** : Proposée, à valider en équipe

## D-06 · Analyse centrée sur le gazole
- **Date** : 2026-10-27
- **Décision** : toutes les questions analytiques portent sur le gazole ; `prix@nom` sert de filtre au chargement.
- **Justification** : carburant des poids lourds du commanditaire (fédération de transporteurs routiers, CDC annexe A.10) ; validé par le commanditaire (Q-02). Comparaisons automatiquement à carburant égal (EF-08) ; volume réduit d'environ 70 % (ET-05).
- **Alternatives écartées** : tous les carburants (hors besoin, plus lourd) ; carburant témoin E10 (non demandé).
- **Statut** : Validée (commanditaire, Q-02)

## D-07 · Choix du périmètre d'analyse (Issue #6)
- **Date** : 2026-10-28
- **Décision** : Région Île-de-France, années 2021 à 2023, le gazole comme unique carburant.
- **Justification** :
  - **Carburant (gazole)** : Pertinence métier (le commanditaire est une fédération de transporteurs routiers, annexe A.10)[cite: 19]. Les comparaisons se font "à carburant égal" pour éviter les biais (EF-08)[cite: 9]. Le volume est réduit (environ 1,5 M de relevés sur 5,3 M, soit ~29%), ce qui est adapté pour un PC de 8 Go (ET-05)[cite: 11].
  - **Région (IDF)** : Permet de compter les stations sur autoroute (condition pour le surcoût, EF-08) et conditionne la viabilité sur 8 Go (ET-05)[cite: 9, 11]. *Limite assumée* : les autoroutes franciliennes sont courtes et très urbaines, le surcoût sera peu généralisable.
  - **Période (2021-2023)** : Indispensable pour voir l'avant-choc (2021), l'année des remises de l'État à la pompe (2022) et la sortie des remises (2023). Ces remises vont créer des ruptures de séries temporelles qu'il faudra tracer.
- **Alternatives écartées** : Analyser tous les carburants. Écarté car cela introduirait un facteur de confusion lors de la comparaison des prix (exigence EF-08). Se restreindre au gazole garantit une comparaison systématique "à carburant égal".
- **Statut** : Validée (équipe)


## D-08 · Seuil minimal de stations par commune (QA-1.2)
- **Date** : 2026-10-28
- **Décision** : une commune n'entre dans le classement de QA-1.2 que si elle compte au moins 5 stations distribuant du gazole sur la période. Paris est traité comme une seule commune (codes postaux 75001 à 75020 regroupés).
- **Justification** : en dessous de 5 stations, une seule station suffit à déplacer fortement la médiane, et le classement mesurerait alors une station plutôt qu'une commune (demande du commanditaire, Q-05). Le seuil est confirmé après comptage : il doit laisser au moins 10 communes classables pour présenter les 5 moins chères et les 5 plus chères. Le nombre de communes retenues et exclues est indiqué à côté du classement.
- **Alternatives écartées** : aucun seuil (classement dominé par les communes à une station) ; seuil de 10 (risque d'exclure presque toute la grande couronne, à vérifier au comptage).
- **Statut** : Proposée, valeur à confirmer après comptage des stations (issue #6)

## D-09 · Écarts exprimés en euros pour un volume de référence
- **Date** : 2026-10-28
- **Décision** : en plus des cts/L et du %, chaque écart est exprimé en euros pour 100 litres de gazole.
- **Justification** : demande du commanditaire (Q-05). Avec 100 L, la conversion est immédiate (1 ct/L = 1 € pour 100 L), ce qui reste lisible par un non-spécialiste ; le résultat se transpose ensuite à n'importe quel volume de flotte.
- **Alternatives écartées** : volume d'un plein de poids lourd ou consommation annuelle d'une flotte (nécessite une source externe, soumise à accord écrit du commanditaire, CDC §3).
- **Statut** : Proposée, à valider en équipe

## D-10 · Format du flux v2 : CSV data.gouv.fr
- **Date** : 2026-10-28
- **Décision** : la description des stations est lue depuis la version CSV du flux v2 publiée sur data.gouv.fr ; l'historique annuel reste en XML (imposé, Q-06).
- **Justification** : format libre pour le flux v2 (Q-06). Même identifiant `id`, même échelle de coordonnées et même code `pop` que l'historique, donc jointure EF-06 directe. Le CSV apporte `Département`, `code_departement` et `Région`, absents de l'historique : la jointure enrichit réellement les données. Lecture avec `pd.read_csv` (vu en cours).
- **Alternatives écartées** : XML du ministère (structure identique à l'historique, mais la jointure n'ajouterait quasiment aucune information).
- **Statut** : Proposée, à valider en équipe
- Le flux peut être téléchargé en `.csv` ou en `.csv.gz` : `pd.read_csv` détecte la compression d'après l'extension, aucun traitement particulier n'est nécessaire dans `charger_stations()`.

## D-11 · Contrat de données des tables nettoyées
- **Date** : 2026-10-28
- **Décision** : les fonctions `nettoyer_*` produisent deux tables au format long (une ligne = un relevé ou une station), avec les colonnes ci-dessous.
  - `data/processed/historique_gazole_idf.parquet` : `id_station` (str), `code_postal` (str), `departement` (str, 2 caractères), `implantation` (str, valeurs de `pop`), `date_releve` (datetime), `prix_gazole` (float, €/L)
  - `data/processed/stations_idf.parquet` : `id_station` (str), `code_postal` (str), `departement` (str), `ville` (str), `implantation` (str), `latitude` (float, degrés), `longitude` (float, degrés)
- **Justification** : 4 personnes codent en parallèle (QC-03) ; mêmes noms et mêmes types pour la jointure (EF-06) ; un seul carburant (D-06), donc pas besoin de format large ; Parquet pour tenir sur 8 Go (ET-05).
- **Alternatives écartées** : format large (une colonne par carburant), inutile avec le seul gazole ; identifiant en entier, qui crée un risque d'échec de jointure entre XML et CSV.
- **Statut** : Proposée (Noé), à valider en relecture de #8

## D-12 · Organisation des notebooks
- **Date** : 2026-10-28
- **Décision** : six notebooks, exécutés dans cet ordre, chacun avec un seul propriétaire :
  - `01_exploration_historique` (Hafsa), `01_exploration_stations` (Thikana), `01_premiers_indicateurs` (Samuel, provisoire)
  - `02_nettoyage_historique` (Samuel), `02_nettoyage_stations` (Noé), `02_jointure` (Noé, co-autrice Thikana)
  - `03_analyse` (Noé) : un seul notebook, car l'analyse porte sur la table jointe des deux sources
  Le code réutilisable vit dans `src/` ; en analyse, chacun écrit ses fonctions dans `src/indicators.py` et le propriétaire de `03_analyse` les appelle.
- **Justification** : un `.ipynb` est un fichier JSON que Git ne sait pas fusionner à deux ; un propriétaire par fichier évite les conflits ; QC-03. Écart à l'annexe B autorisé s'il est décrit dans le README.
- **Alternatives écartées** : un notebook unique pour tout le projet (conflits à chaque PR) ; plusieurs notebooks d'analyse (les deux sources doivent être croisées dans la même table).
- **Statut** : Validée en équipe le 2026-11-19 (commentaire sur #47)

## D-13 · Calcul de l'écart de prix entre départements (QA-1.1)
- **Date** : 2026-10-30
- **Décision** : pour chaque station, calculer la médiane de ses prix hebdomadaires, puis calculer la médiane de ces valeurs par département ; exprimer l'écart de chaque département en cts/L et en % par rapport au département ayant la médiane la plus basse. Dans `prix_median_hebdo()`, `nb_stations` compte les stations ayant un prix la semaine concernée, pas les stations présentes dans la table.
- **Justification** : QA-1.1 demande les prix médians par département et l'écart entre le moins cher et le plus cher (`docs/questions.md`). Une médiane par station évite de donner davantage de poids aux stations ayant plus de semaines renseignées. La différence entre la médiane maximale et minimale donne l'écart demandé ; le pourcentage est rapporté au prix du département le moins cher.
- **Alternatives écartées** : comparer chaque département à la médiane régionale, qui ne répond pas à la comparaison du moins cher au plus cher ; calculer une médiane départementale directement sur toutes les semaines-stations, ce qui surpondérerait les stations ayant davantage de relevés.
- **Statut** : Validée en équipe le 2026-11-19 (commentaire sur #47)

## D-14 · Pose tardive des tags v0.1 et v0.2
- **Date** : 2026-11-16
- **Décision** : `v0.1` est posé sur le merge de la PR #18 et `v0.2` sur celui de la PR #33, tous deux le 16/11.
- **Justification** : GIT-06 impose un tag par jalon ; on tague le premier état de `main` qui contient les livrables du jalon, sans réécrire l'historique.
- **Alternatives écartées** : ne pas poser les tags manqués (exigence non remplie) ; les poser sur `main` actuel (ne reflète pas l'état au jalon).
- **Statut** : Validée en équipe le 2026-11-19 (commentaire sur #47)

## D-15 · Choix de l'outil du tableau de bord (ET-03)
- **Date** : 2026-11-16
- **Décision** : réaliser le tableau de bord avec Streamlit, dans une seule page `app/dashboard.py`, lancée par `streamlit run app/dashboard.py`. La version est figée dans `requirements.txt` (`streamlit==1.66.1`).
- **Justification** : ET-03 impose Streamlit par défaut et n'autorise Dash ou Panel que sur demande validée en S44 ; aucune demande n'a été faite. TB-06 demande un lancement en une commande et un affichage en moins de 10 s, ce que permet la page minimale. ET-05 demande de rester léger pour un portable de 8 Go de RAM : Streamlit lit directement les fichiers Parquet avec pandas. ET-01 est respectée par la version figée dans `requirements.txt`.
- **Alternatives écartées** : Dash et Panel, qui ne sont autorisés que sur demande validée en S44 (ET-03) et pour lesquels l'équipe n'a aucun besoin justifiant une dérogation.
- **Statut** : Validée en équipe le 2026-11-19 (commentaire sur #47)

## D-16 · Doublons fonctionnels de l'historique : garder la dernière ligne
- **Date** : 2026-11-17
- **Décision** : pour deux relevés de la même station au même instant, on garde la dernière ligne du fichier (`keep="last"`), dans `nettoyer_historique()`.
- **Justification** : 8 lignes supprimées sur 587 090 lignes brutes (ANO-04) ; solution simple (`drop_duplicates`, vu en cours) qui conserve une valeur réelle de la source.
- **Alternatives écartées** : moyenne des deux prix (valeur qui n'existe pas dans la source) ; double `NaN` (perte de relevés réels).
- **Statut** : Validée en équipe le 2026-11-19 (commentaire sur #47)

## D-17 · Traitement des prix aberrants de l'historique, année par année
- **Date** : 2026-11-17
- **Décision** : dans `nettoyer_historique()`, appelée une année à la fois, les valeurs suivantes passent en `NaN` (la ligne est conservée), dans cet ordre : prix hors du seuil métier (< 1 € ou > 3 €), prix sous la borne basse 1,5 × IQR, prix supérieur à 1,5 fois la médiane de sa station.
- **Justification** : les trois années n'ont pas le même niveau de prix (médianes de 1,499 € en 2021, 1,903 € en 2022 et 1,872 € en 2023), donc les bornes se calculent par année (ANO-05, ANO-07). Les prix élevés de mars et octobre 2022 et de septembre-octobre 2023 sont des chocs de marché (D-07) : la borne haute est relative à la station, pas un IQR global (ANO-03).
- **Alternatives écartées** : IQR sur les trois années réunies ; borne haute à 1,3 × la médiane de la station (écarterait 63 relevés de 2022 qui semblent réels) ; suppression des lignes (interdit sans fiche ANO, CDC §8).
- **Statut** : Validée en équipe le 2026-11-19 (commentaire sur #47) Le seuil de 1,5 a été fixé après examen des données : en 2021 et en 2023, un vide sépare le dernier ratio plausible (1,2 à 1,4) des valeurs écartées (au moins 1,535) ; en 2022, aucun relevé ne dépasse 1,394.

## D-18 · Département retenu après la jointure
- **Date** : 2026-11-17
- **Décision** : pour les stations retrouvées dans le flux v2, le département est celui du flux (`code_departement`) ; pour les 121 stations absentes du flux (ANO-13), c'est celui déduit des 2 premiers chiffres du code postal dans l'historique. La table jointe est enregistrée dans `data/processed/historique_joint_idf.parquet` ; c'est elle que lisent `03_analyse` et le tableau de bord.
- **Justification** : ANO-12 montre que le code postal peut appartenir à un autre département ; le flux est la seule source officielle, mais il ne décrit pas les stations fermées. Garder ces stations évite le biais du survivant sur QA-4.
- **Alternatives écartées** : utiliser partout le code postal (erreur connue, ANO-12) ; exclure les stations absentes du flux (biais du survivant, 7,8 % des relevés).
- **Statut** : Validée en équipe le 2026-11-19 (commentaire sur #47)

## D-20 · Prix supposé inchangé entre deux relevés (QA-2.3)
- **Date** : 2026-11-19
- **Décision** : pour comparer les jours de la semaine, chaque station reçoit un prix par jour : le dernier prix publié dans la journée, sinon le dernier prix connu de la station, au plus 7 jours après son dernier relevé.
- **Justification** : un relevé correspond à une publication de prix, pas à une vente ; les stations publient moins le week-end (dimanche : 9,0 % des relevés et 770 stations, contre environ 905 en semaine), donc la médiane des relevés bruts par jour compare des groupes de stations différents. 7 jours couvrent un cycle complet de semaine ; au-delà, la station a pu fermer.
- **Alternatives écartées** : médiane des relevés bruts par jour (biaisée, voir ci-dessus) ; remplissage sans limite (prolonge le prix des stations fermées).
- **Statut** : Proposée (Noé), à valider en équipe
## D-19 · Seuil minimal de stations d'autoroute par département (QA-3.3)
- **Date** : 2026-11-19
- **Décision** : un département n'est interprété dans QA-3.3 que s'il compte au moins 5 stations A (hors station N). Les départements sous le seuil restent dans le tableau avec leurs effectifs, marqués `interprete = False`, et ne sont pas commentés. Le seuil est le paramètre `seuil_stations_a` de `ecart_autoroute_par_departement()`.
- **Justification** : en dessous de 5 stations A, la médiane hebdomadaire A repose sur une ou deux stations : l'écart mesurerait une station plutôt que l'autoroute du département. Même raisonnement et même valeur que D-08 pour les communes. Le seuil est fixé d'après le nombre de stations A par département (77 : 17, 91 : 9, 78 : 7, 95 : 6, 94 : 3, 93 : 2, 92 : 1) et non d'après les valeurs des écarts. Q-05 demande d'indiquer le nombre de stations derrière chaque comparaison.
- **Alternatives écartées** : aucun seuil (le 93, avec 2 stations A, serait commenté comme le 77, qui en a 17) ; seuil de 10 (ne garderait que le 77) ; seuil de 3 (garderait le 94, dont la médiane repose sur 3 stations).
- **Statut** : Proposée (Thikana), à valider en équipe
