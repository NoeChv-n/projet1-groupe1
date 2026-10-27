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
- **Statut** : Proposée, à valider en équipe

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
