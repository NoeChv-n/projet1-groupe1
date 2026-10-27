# Journal des anomalies — Groupe 1

> **Règle** : aucune ligne n'est supprimée ou corrigée sans fiche ici (CDC §8).
> Une anomalie non traitée est acceptable si elle est documentée et que son impact est énoncé. Une anomalie connue mais tue est un motif de refus en recette.

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