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


## ANO-10 · Région, ville et département manquants pour 4 stations
- **Colonne(s)** : `Région`, `Ville`, `code_departement`
- **Description** : les trois colonnes sont vides ensemble pour 4 stations.
  Exemple : id 76600022, Code postal 76600, Région = NaN.
- **Ampleur** : 4 lignes sur 9 829 (≈ 0,04 %)
- **Cause probable** : rattachement géographique non renseigné dans la source.
- **Traitement proposé** : signaler, ne rien corriger. Leurs codes postaux
  (76600, 56700, 83150, 83380) sont hors Île-de-France : le filtre les exclut
  à raison.
- **Impact sur l'analyse** : aucun sur le périmètre Île-de-France.

## ANO-11 · Coordonnées stockées en entiers
- **Colonne(s)** : `latitude`, `longitude`
- **Description** : valeurs en entiers, ex. latitude 4883600, longitude 235927.
- **Ampleur** : 831 lignes sur 831 en Île-de-France (100 %)
- **Cause probable** : format de la source (degrés × 100 000)
- **Traitement proposé** : diviser par 100 000 dans `nettoyer_stations()`,
  puis vérifier : latitude entre 48 et 49,2, longitude entre 1,4 et 3,6
- **Impact sur l'analyse** : cartes et distances faussées si non converties