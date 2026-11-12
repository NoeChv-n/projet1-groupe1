# Journal des anomalies — Groupe 1

> **Règle** : aucune ligne n'est supprimée ou corrigée sans fiche ici (CDC §8).
> Une anomalie non traitée est acceptable si elle est documentée et que son impact est énoncé. Une anomalie connue mais tue est un motif de refus en recette.

> **Plages réservées** (pour ne pas écrire au même endroit) : ANO-01 à ANO-09 pour l'historique (Hafsa), ANO-10 et suivantes pour le flux des stations (Thikana). Les anomalies de jointure prennent la suite de la plage flux.

## Récapitulatif

| ID | Colonne(s) | Résumé | Ampleur | Traitement |
|---|---|---|---|---|
| — | — | Aucune anomalie consignée pour l'instant | — | — |

## Contrôles minimaux (CDC §8)

- [ ] 1. Doublons exacts et doublons fonctionnels (même station / même relevé décrit plusieurs fois)
- [ ] 2. Valeurs manquantes, y compris déguisées (0, chaîne vide, « -1 »)
- [ ] 3. Types incohérents (dates en texte, codes postaux sans zéro initial, prix et coordonnées en entiers)
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
- **Description** : Présence de prix impossibles sur le marché (ex: 0.100 €/L et 0.190 €/L à Courbevoie). Détecté lors de l'exploration EF-03 via la règle 1,5 x IQR (sous la limite basse de 1.56 €).
- **Ampleur** : Fait partie des 680 relevés hors domaine détectés sur 175 351 lignes.
- **Cause probable** : Erreurs de frappe ou de placement de virgule lors de la saisie par la station.
- **Traitement** : Remplacer ces valeurs par du vide (`NaN`) ou appliquer une correction si l'erreur de virgule est évidente.
- **Impact** : Fausse la moyenne à la baisse si ce n'est pas nettoyé.

## ANO-03 · Prix du gazole anormalement hauts (2023)
- **Colonne(s)** : `prix`
- **Description** : Présence de prix extrêmes (ex: 7.760 €/L et 7.719 €/L à Bonneuil-sur-Marne). Détecté via la règle 1,5 x IQR (au-dessus de la limite haute de 2.19 €).
- **Ampleur** : Fait partie des 680 relevés hors domaine détectés sur l'année 2023.
- **Cause probable** : Erreur de saisie.
- **Traitement** : Remplacer par `NaN`.
- **Impact** : Tire la moyenne artificiellement vers le haut.

## ANO-10 · Région, ville et département manquants pour 4 stations
- **Colonne(s)** : `Région`, `Ville`, `code_departement`
- **Description** : les trois colonnes sont vides ensemble pour 4 stations.
  Exemple : id 76600022, Code postal 76600, Région = NaN.
- **Ampleur** :  4 lignes sur 9 826 (≈ 0,04 %)
- **Cause probable** : rattachement géographique non renseigné dans la source.
- **Traitement proposé** : signaler, ne rien corriger. Leurs codes postaux
  (76600, 56700, 83150, 83380) sont hors Île-de-France : le filtre les exclut
  à raison.
- **Impact sur l'analyse** : aucun sur le périmètre Île-de-France.

## ANO-11 ·  Coordonnées GPS dans une unité non standard (degrés × 100 000)
- **Colonne(s)** : `latitude`, `longitude`
- **Description** : valeurs en degrés × 100 000, parfois avec décimales, ex. latitude 4883600, longitude 235927.279911.
- **Ampleur** : 831 lignes sur 831 en Île-de-France (100 %)
- **Cause probable** : format de la source (degrés × 100 000)
- **Traitement proposé** : diviser par 100 000 dans `nettoyer_stations()`,
  puis vérifier : latitude entre 48 et 49,2, longitude entre 1,4 et 3,6
- **Impact sur l'analyse** : cartes et distances faussées si non converties

## ANO-12 · Code postal incohérent avec le département
- **Colonne(s)** : `Code postal`, `code_departement`
- **Description** : les 2 premiers chiffres du code postal diffèrent du
  département pour 4 stations.
  Exemples : id 78800001, Bezons, code postal 78800, département 95 ;
  id 94160001, Paris, code postal 94160, département 75.
- **Ampleur** : 4 lignes sur 831 en Île-de-France (≈ 0,5 %)
- **Cause probable** : pour 3 cas, découpage postal différent du découpage
  administratif (à vérifier) ; pour id 94160001 (Paris / 94160),
  possible erreur de saisie.
- **Traitement proposé** : conserver les 4 lignes ; utiliser
  `code_departement` pour tout regroupement par département, jamais les
  2 premiers chiffres du code postal ; vérifier id 94160001 à la source.
- **Impact sur l'analyse** : regroupements par département faussés si on
  se base sur le code postal ; effet limité (4 stations).

  ## ANO-13 · Stations de l'historique 2021 absentes du flux actuel
- **Colonne(s)** : `id` (historique 2021 et flux v2)
- **Description** : des stations de l'historique 2021 n'ont plus de ligne dans le flux v2 du 09/11/2026. Exemple : id ... (à compléter avec absents_idf.head()).
- **Ampleur** : en Île-de-France, 838 lignes sur 1 607 (≈ 52 %), dont 798 en route et 40 en autoroute. En France, 5 016 sur 13 386 (≈ 37 %).
- **Cause probable** : stations fermées depuis 2021, changement d'identifiant ou absence de prix récents. Les données seules ne permettent pas de trancher.
- **Traitement proposé** : signaler et conserver. Lors de la jointure (EF-06), garder ces stations avec leur identifiant, sans les supprimer, et compter les identifiants non retrouvés.
- **Impact sur l'analyse** : ces stations n'ont ni ville ni département officiels. Leur type de route et leur code postal viennent de l'historique. Le périmètre Île-de-France est estimé par les 2 premiers chiffres du code postal (voir ANO-12), donc le chiffre est un ordre de grandeur. Seule l'année 2021 est examinée, pas 2022 ni 2023.

## ANO-14 · Valeur de pop hors domaine dans l'historique 2021
- **Colonne(s)** : `pop`
- **Description** : `pop` vaut `N` pour 2 stations alors que le flux n'a que `R` et `A`. Exemples : id 13500010 (code postal 13500), id 95320005 (code postal 95320).
- **Ampleur** : 2 lignes sur 13 386 (≈ 0,01 %).
- **Cause probable** : code non documenté ou erreur de saisie, à vérifier dans la documentation du producteur.
- **Traitement proposé** : signaler et conserver. Ne pas classer ces stations en route ou autoroute avant vérification.
- **Impact sur l'analyse** : négligeable (2 stations, dont 1 en Île-de-France), mais elles sont à exclure des comparaisons route/autoroute.
