# Journal des anomalies — Groupe 1

> **Règle** : aucune ligne n'est supprimée ou corrigée sans fiche ici (CDC §8).
> Une anomalie non traitée est acceptable si elle est documentée et que son impact est énoncé. Une anomalie connue mais tue est un motif de refus en recette.

> **Plages réservées** (pour ne pas écrire au même endroit) : ANO-01 à ANO-09 pour l'historique (Hafsa), ANO-10 et suivantes pour le flux des stations (Thikana). Les anomalies de jointure prennent la suite de la plage flux.

## Récapitulatif

| ID     | Colonne(s) | Résumé                                   | Ampleur               | Traitement          |
| ------ | ---------- | ---------------------------------------- | --------------------- | ------------------- |
| ANO-02 | `prix`| Prix du gazole < 1 € (2023) | 22 relevés sur 175 351 (≈ 0,01 %) | `NaN` si prix < 1 € |
| ANO-03 | `prix`| Prix du gazole > 3 € et pics plausibles (2023) | 631 relevés sur 175 351 (≈ 0,36 %) | `NaN` si prix > 3 €, le reste conservé |
| ANO-10 | `Région`, `Ville`, `code_departement` | 4 stations sans rattachement géographique | 4 / 9 820 (0,04 %) | Signalé, exclu par le filtre IDF |
| ANO-11 | `latitude`, `longitude` | Coordonnées en degrés × 100 000 | 833 / 833 (100 %) | Corrigé (÷ 100 000) |
| ANO-12 | `Code postal`, `code_departement` | Code postal d'une autre commune que le département | 4 / 833 (0,5 %) | Conservé, `departement` utilisé |
| ANO-13 | `id` | Stations de l'historique absentes du flux | 838 / 1 607 IDF (52 %) | Proposé : conservé à la jointure |
| ANO-14 | `pop` | Valeur `N` hors domaine dans l'historique | 2 / 13 386 (0,01 %) | Proposé : exclu de route/autoroute |

## Contrôles minimaux (CDC §8)

- [ ] 1. Doublons exacts et doublons fonctionnels (même station / même relevé décrit plusieurs fois) — flux IDF : 0 doublon exact, 0 id en double (#27)
- [ ] 2. Valeurs manquantes, y compris déguisées (0, chaîne vide, « -1 ») — flux IDF : 0 coordonnée manquante ou illisible (#27)
- [ ] 3. Types incohérents (dates en texte, codes postaux sans zéro initial, prix et coordonnées en entiers) — flux IDF : codes postaux à 5 caractères, coordonnées converties (#27, ANO-11)
- [ ] 4. Valeurs hors domaine ou aberrantes (méthode : 1,5 × IQR et/ou seuil métier, à préciser)
- [ ] 5. Ruptures de série (carburants apparus/disparus, format XML qui change, remises 2022)
- [ ] 6. Couverture (périodes ou territoires absents ou partiels)

---

## Modèle de fiche (à copier pour chaque anomalie)

### ANO-xx · Titre court

- **Colonne(s) concernée(s)** : nom exact dans la source
- **Description** : ce qui est observé, avec un exemple de valeur
- **Ampleur** : nombre de lignes et part du total (%)
- **Cause probable** : erreur de saisie, changement de nomenclature, doublon structurel…
- **Traitement retenu** : conservé / corrigé / imputé / exclu / signalé — avec la justification
- **Impact sur l'analyse** : indicateurs ou conclusions affectés
- **Détectée par / date** : Prénom, AAAA-MM-JJ · lien vers la PR

## ANO-01 · Format variable du flux v2 téléchargé

- **Colonne(s)** : fichier entier (`data/raw/flux_v2.csv`)
- **Description** : la même URL data.gouv renvoie tantôt un CSV compressé gzip (3,0 Mo), tantôt un CSV en clair UTF-8 avec BOM (19 Mo). Constaté le 2026-10-28 avec `file`.
- **Ampleur** : 1 fichier, aléatoire selon le téléchargement
- **Cause probable** : comportement du serveur de diffusion (compression non systématique)
- **Traitement** : fichier enregistré sous un nom neutre ; la lecture tente gzip puis bascule sur le texte brut (`gzip.BadGzipFile`), avec `encoding="utf-8-sig"` pour le BOM
- **Impact** : aucun sur l'analyse si la lecture gère les deux cas ; sans ce traitement, le chargement échoue une fois sur deux

## ANO-02 · Prix du gazole anormalement bas (2023)

- **Colonne(s)** : `prix`
- **Description** : Présence de prix impossibles sur le marché (seuil métier : prix < 1 €, dont 0.100 € et 0.190 €).
- **Ampleur** : 22 relevés sur 175 351 (soit ~0,01 %).
- **Cause probable** : Erreurs de frappe ou de placement de virgule lors de la saisie par la station.
- **Traitement** : Remplacer par du vide (`NaN`) les valeurs strictement inférieures à 1 €.
- **Impact** : Fausse la moyenne à la baisse si ce n'est pas nettoyé.

## ANO-03 · Prix du gazole anormalement hauts (2023)

- **Colonne(s)** : `prix`
- **Description** : Présence de prix impossibles (seuil métier : > 3 €, dont 7.76 €) et de prix très hauts mais plausibles liés au pic de septembre-octobre 2023 (entre 2,19 € et 2,95 €).
- **Ampleur** : 631 relevés au-dessus de 2,19 € sur 175 351 (≈ 0,36 %) : 3 relevés impossibles (> 3 €) et 628 relevés plausibles.
- **Cause probable** : Erreur de saisie pour les prix > 3 €. Contexte économique réel pour les prix entre 2,19 € et 2,62 € (majoritairement Paris et autoroutes).
- **Traitement** : Remplacer par du vide (`NaN`) les valeurs strictement supérieures à 3 €. Conserver les prix compris entre 2,19 € et 2,62 €.
- **Impact** : Supprimer les valeurs entre 2,19 € et 2,62 € fausserait les analyses sur Paris et les autoroutes (H-1 et H-2).

## ANO-10 · Région, ville et département manquants pour 4 stations
- **Colonne(s)** : `Région`, `Ville`, `code_departement`
- **Description** : les trois colonnes sont vides ensemble pour 4 stations.
  Exemple : id 76600022, Code postal 76600, Région = NaN.
- **Ampleur** : 4 lignes sur 9 820 (≈ 0,04 %), flux du [11/11/2026]
  (4 sur 9 826 lors de l'exploration : le flux change à chaque téléchargement).
- **Cause probable** : rattachement géographique non renseigné dans la source.
- **Traitement retenu** : signalé, aucune correction. Sans département, ces
  stations sont écartées par le filtre `code_departement` de `charger_stations()`.
  Leurs codes postaux (76600, 56700, 83150, 83380) sont hors Île-de-France :
  l'exclusion est correcte.
- **Impact sur l'analyse** : aucun sur le périmètre Île-de-France.
- **Détectée par / date** : Thikana, [11/11/2026] · traitée par Noé, 2026-11-16 (#27)

## ANO-11 · Coordonnées GPS dans une unité non standard (degrés × 100 000)
- **Colonne(s)** : `latitude`, `longitude`
- **Description** : valeurs en degrés × 100 000, parfois avec décimales,
  ex. latitude 4883600, longitude 235927.279911.
- **Ampleur** : 833 lignes sur 833 en Île-de-France (100 %), flux du [11/11/2026]
  (831 lors de l'exploration).
- **Cause probable** : format de la source (degrés × 100 000).
- **Traitement retenu** : corrigé dans `nettoyer_stations()` : conversion en
  nombre (`pd.to_numeric`, `errors="coerce"`) puis division par 100 000.
  Contrôles après conversion : 0 valeur manquante, 0 station hors des bornes
  (latitude 48 à 49,2 ; longitude 1,4 à 3,6). Valeurs observées : latitude
  48,145 à 49,157 ; longitude 1,489 à 3,361.
- **Impact sur l'analyse** : aucun après correction ; coordonnées utilisables
  pour les cartes et les distances.
- **Détectée par / date** : Thikana, [11/11/2026] · traitée par Noé, 2026-11-16 (#27)

## ANO-12 · Code postal incohérent avec le département
- **Colonne(s)** : `Code postal`, `code_departement`
- **Description** : les 2 premiers chiffres du code postal diffèrent du
  département pour 4 stations : 78800001 (Bezons, 78800, dép. 95),
  92120004 (Le Kremlin-Bicêtre, 92120, dép. 94), 94160001 (Paris, 94160,
  dép. 75), 94542003 (Paray-Vieille-Poste, 94542, dép. 91).
- **Ampleur** : 4 lignes sur 833 en Île-de-France (≈ 0,5 %), flux du [11/11/2026].
- **Cause probable** : dans 3 cas, la ville et le département sont cohérents
  entre eux et c'est le code postal qui correspond à une commune voisine
  (Bezons / 78800, Le Kremlin-Bicêtre / 92120) ou à un code CEDEX
  (Paray-Vieille-Poste / 94542). Pour id 94160001 (Paris / 94160), la station
  est à la limite Paris / Saint-Mandé : non tranché. Hypothèses à vérifier,
  non issues des données.
- **Traitement retenu** : conservé, aucune correction. Dans `nettoyer_stations()`,
  `departement` est copié depuis `code_departement`, jamais calculé à partir
  du code postal. Le code postal n'est pas modifié, faute de source pour le corriger.
- **Impact sur l'analyse** : aucun sur les regroupements par département.
  Risque pour D-08 : Paris y est regroupé par codes postaux 75001 à 75020,
  la station 94160001 n'y serait donc pas comptée. À traiter à la jointure
  ou en analyse.
- **Détectée par / date** : Thikana, [11/11/2026] · traitée par Noé, 2026-11-16 (#27)

## ANO-13 · Stations de l'historique 2021 absentes du flux actuel
- **Colonne(s)** : `id` (historique 2021 et flux v2)
- **Description** : des stations de l'historique 2021 n'ont plus de ligne dans
  le flux v2 du 09/11/2026. Exemple : le flux v2 du 09/11/2026. Exemple : id 75005001.
- **Ampleur** : en Île-de-France, 838 lignes sur 1 607 (≈ 52 %), dont 798 en
  route et 40 en autoroute (flux du 09/11/2026) ; recompté avec le flux du
  11/11/2026 : 836 sur 1 607 (≈ 52 %), dont 796 en route et 40 en autoroute.
  En France, 5 016 sur 13 386 (≈ 37 %) (flux du 09/11/2026).
- **Cause probable** : stations fermées depuis 2021, changement d'identifiant ou
  absence de prix récents. Les données seules ne permettent pas de trancher.
- **Traitement proposé** : signaler et conserver. Lors de la jointure (EF-06),
  garder ces stations avec leur identifiant, sans les supprimer, et compter
  les identifiants non retrouvés.
- **Impact sur l'analyse** : ces stations n'ont ni ville ni département
  officiels. Leur type de route et leur code postal viennent de l'historique.
  Le périmètre Île-de-France est estimé par les 2 premiers chiffres du code
  postal (voir ANO-12), donc le chiffre est un ordre de grandeur. Seule l'année
  2021 est examinée, pas 2022 ni 2023.
- **Suivi** : sans objet pour `nettoyer_stations()` (#27) : aucune ligne du
  flux n'est concernée. Traitement à appliquer dans `02_jointure`.
- **Détectée par / date** : Thikana, [11/11/2026]

## ANO-14 · Valeur de pop hors domaine dans l'historique 2021
- **Colonne(s)** : `pop`
- **Description** : `pop` vaut `N` pour 2 stations alors que le flux n'a que
  `R` et `A`. Exemples : id 13500010 (code postal 13500), id 95320005
  (code postal 95320).
- **Ampleur** : 2 lignes sur 13 386 (≈ 0,01 %).
- **Cause probable** : code non documenté ou erreur de saisie, à vérifier dans
  la documentation du producteur.
- **Traitement proposé** : signaler et conserver. Ne pas classer ces stations
  en route ou autoroute avant vérification.
- **Impact sur l'analyse** : négligeable (2 stations, dont 1 en Île-de-France),
  mais elles sont à exclure des comparaisons route/autoroute.
- **Suivi** : sans objet pour `nettoyer_stations()` (#27) : le flux du
  [JJ/MM/2026] ne contient que R (795) et A (38), vérifié par un `assert`
  dans la fonction. Traitement à appliquer dans `nettoyer_historique()`
  (Samuel, #14) ou à la jointure.
- **Détectée par / date** : Thikana, [11/11/2026]