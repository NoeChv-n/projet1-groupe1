# Questions — Groupe 1

## 1. Questions analytiques (EF-01)

> Version v1 (issue #5). Carburant retenu : gazole (D-06). Chaque sous-question est reliée aux colonnes qui permettent d'y répondre.

**Question principale** : pour réduire la dépense en gazole d'une flotte dans la région retenue, quels écarts de prix au litre observe-t-on selon le lieu, le moment et le type de route, et comment ces prix ont-ils évolué sur la période retenue ?

### QA-1 · Où le gazole est-il le moins cher dans la région ?
| N° | Sous-question | Colonnes / variables | Indicateur | Statut |
|---|---|---|---|---|
| QA-1.1 | Quel est le prix médian par département, et quel écart sépare le moins cher du plus cher ? | `cp`, `prix@nom`, `prix@valeur` | Prix médian (€/L), écart en cts et en % | Brouillon |
| QA-1.2 | Quelles communes (≥ n stations) ont les prix médians les plus bas et les plus élevés ? | `ville`, `cp`, `prix@nom`, `prix@valeur` | Prix médian (€/L), classement | Brouillon |
| QA-1.3 | Les prix sont-ils plus dispersés dans certains départements que dans d'autres ? | `cp`, `prix@nom`, `prix@valeur` | Écart interquartile (cts) | Brouillon |

### QA-2 · À quel moment le plein coûte-t-il le moins cher ?
| N° | Sous-question | Colonnes / variables | Indicateur | Statut |
|---|---|---|---|---|
| QA-2.1 | Quel est l'écart entre le prix médian de chaque mois et le prix médian de son année ? | `prix@maj`, `prix@nom`, `prix@valeur` | Écart mensuel en cts et en % | Brouillon |
| QA-2.2 | Ce profil mensuel se retrouve-t-il d'une année sur l'autre ? | `prix@maj`, `prix@nom`, `prix@valeur` | Écarts mensuels comparés par année | Brouillon |
| QA-2.3 | Le prix médian diffère-t-il selon le jour de la semaine ? | `prix@maj`, `prix@nom`, `prix@valeur` | Écart par jour en cts | À confirmer après exploration |

### QA-3 · Quel est le surcoût réel de l'autoroute ?
| N° | Sous-question | Colonnes / variables | Indicateur | Statut |
|---|---|---|---|---|
| QA-3.1 | À semaine identique, quel est l'écart de prix médian entre stations d'autoroute et hors autoroute ? | `pop`, `prix@maj`, `prix@nom`, `prix@valeur` | Écart hebdomadaire en cts et en % | Brouillon |
| QA-3.2 | Cet écart est-il stable dans le temps ? | `pop`, `prix@maj`, `prix@nom`, `prix@valeur` | Évolution de l'écart (cts) | Brouillon |
| QA-3.3 | Cet écart varie-t-il selon le département (si les effectifs le permettent) ? | `pop`, `cp`, `prix@maj`, `prix@nom`, `prix@valeur` | Écart en cts par département | Brouillon |

### QA-4 · Comment le prix a-t-il évolué sur la période ?
| N° | Sous-question | Colonnes / variables | Indicateur | Statut |
|---|---|---|---|---|
| QA-4.1 | Comment le prix médian hebdomadaire a-t-il évolué sur la période retenue ? | `prix@maj`, `prix@nom`, `prix@valeur` | Prix médian hebdomadaire (€/L) | Brouillon |
| QA-4.2 | Quelles sont les semaines de plus forte hausse et de plus forte baisse, et quelle est leur ampleur ? | `prix@maj`, `prix@nom`, `prix@valeur` | Variation hebdomadaire en cts et en % | Brouillon |
| QA-4.3 | Ces périodes coïncident-elles avec des événements datés (voir Q-04) ? | `prix@maj`, `prix@valeur` + dates d'événements | Comparaison descriptive, sans lien causal | Brouillon |

---

## 2. Échanges avec le commanditaire

> Les questions sont posées **par écrit** par l'interlocuteur unique (chef de projet), regroupées, et leur réponse est archivée ici.

### Q-01 · Utilisation d'un LLM comme assistant
- **Date de la question** : 2026-10-26
- **Posée par** : Noé Chauvin
- **Question** : l'équipe peut-elle utiliser un LLM pour l'accompagner pendant le projet ?
- **Réponse** : validée, sous deux réserves :
  1. le LLM n'écrit jamais directement dans les fichiers du dépôt ;
  2. les notions transmises par le LLM doivent être assimilées par l'étudiant (code explicable ligne par ligne en revue).
- **Date de la réponse** : 2026-10-26
- **Conséquence** : mise en place d'instructions communes (`docs/instructions-llm.md`) et d'un workflow par projet Claude / Gem → voir D-04.