# Questions — Groupe 1

## 1. Questions analytiques (EF-01)

> Version **v1 validée par le commanditaire le 2026-10-28, sous réserves** (voir Q-05). Carburant : gazole (D-06). Période : 2021 à 2023 (D-07). Région : Île-de-France (validée, Q-06).
> **Règle** : toute modification ultérieure d'une question ou sous-question est soumise par écrit au commanditaire avant d'être appliquée (Q-05, CDC §3).

**Question principale** : pour réduire la dépense en gazole d'une flotte dans la région retenue, quels écarts de prix au litre observe-t-on selon le lieu, le moment et le type de route, et comment ces prix ont-ils évolué sur la période retenue ?

### QA-1 · Où le gazole est-il le moins cher dans la région ?

| N°     | Sous-question                                                                                                                       | Colonnes / variables                     | Indicateur                                                    | Statut                                            |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------- |
| QA-1.1 | Quel est le prix médian par département, et quel écart sépare le moins cher du plus cher ?                                          | `cp`, `prix@nom`, `prix@valeur`          | Prix médian (€/L), écart en cts et en %                       | Validée                                           |
| QA-1.2 | Parmi les communes qui comptent au moins 5 stations (seuil D-08), lesquelles ont les prix médians les plus bas et les plus élevés ? | `ville`, `cp`, `prix@nom`, `prix@valeur` | Prix médian (€/L), classement, nombre de stations par commune | Validée (Q-05) — seuil à confirmer après comptage |
| QA-1.3 | Les prix sont-ils plus dispersés dans certains départements que dans d'autres ?                                                     | `cp`, `prix@nom`, `prix@valeur`          | Écart interquartile (cts)                                     | Validée                                           |

### QA-2 · À quel moment le plein coûte-t-il le moins cher ?

| N°     | Sous-question                                                                         | Colonnes / variables                  | Indicateur                         | Statut                                                                                            |
| ------ | ------------------------------------------------------------------------------------- | ------------------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------- |
| QA-2.1 | Quel est l'écart entre le prix médian de chaque mois et le prix médian de son année ? | `prix@maj`, `prix@nom`, `prix@valeur` | Écart mensuel en cts et en %       | Validée                                                                                           |
| QA-2.2 | Ce profil mensuel se retrouve-t-il d'une année sur l'autre ?                          | `prix@maj`, `prix@nom`, `prix@valeur` | Écarts mensuels comparés par année | Validée                                                                                           |
| QA-2.3 | Le prix médian diffère-t-il selon le jour de la semaine ?                             | `prix@maj`, `prix@nom`, `prix@valeur` | Écart par jour en cts              | Validée (Q-05), exploratoire : si les données ne permettent pas de conclure, on explique pourquoi |

### QA-3 · Quel est le surcoût réel de l'autoroute ?

| N°     | Sous-question                                                                                       | Colonnes / variables                               | Indicateur                                                                               | Statut         |
| ------ | --------------------------------------------------------------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------------------------------------- | -------------- |
| QA-3.1 | À semaine identique, quel est l'écart de prix médian entre stations d'autoroute et hors autoroute ? | `pop`, `prix@maj`, `prix@nom`, `prix@valeur`       | Écart hebdomadaire en cts, en % et en € (D-09) ; **nombre de stations de chaque groupe** | Validée (Q-05) |
| QA-3.2 | Cet écart est-il stable dans le temps ?                                                             | `pop`, `prix@maj`, `prix@nom`, `prix@valeur`       | Évolution de l'écart (cts) ; **nombre de stations d'autoroute par période**              | Validée (Q-05) |
| QA-3.3 | Cet écart varie-t-il selon le département (si les effectifs le permettent) ?                        | `pop`, `cp`, `prix@maj`, `prix@nom`, `prix@valeur` | Écart en cts par département ; **nombre de stations d'autoroute par département**        | Validée (Q-05) |

### QA-4 · Comment le prix a-t-il évolué sur la période ?

| N°     | Sous-question                                                                                         | Colonnes / variables                                    | Indicateur                                                                  | Statut         |
| ------ | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------- | --------------------------------------------------------------------------- | -------------- |
| QA-4.1 | Comment le prix médian hebdomadaire a-t-il évolué sur la période retenue ?                            | `prix@maj`, `prix@nom`, `prix@valeur`                   | Prix médian hebdomadaire (€/L)                                              | Validée        |
| QA-4.2 | Quelles sont les semaines de plus forte hausse et de plus forte baisse, et quelle est leur ampleur ?  | `prix@maj`, `prix@nom`, `prix@valeur`                   | Variation hebdomadaire en cts et en %                                       | Validée        |
| QA-4.3 | Ces périodes coïncident-elles avec des événements datés à partir d'une source officielle référencée ? | `prix@maj`, `prix@valeur` + dates d'événements sourcées | Comparaison descriptive, sans lien causal ; chaque événement avec sa source | Validée (Q-05) |

---

## 1 bis. Hypothèses formulées avant calcul (EF-05)

> H-1 à H-3 rédigées le 2026-10-28, avant tout calcul sur le périmètre retenu. H-4 ajoutée le 2026-11-19 (#44), avant tout calcul sur QA-2. Le résultat (confirmée / infirmée / non concluante) est ajouté après analyse, sans modifier l'énoncé.


| ID | Hypothèse | Sous-question | Indicateur | Méthode de comparaison descriptive | Ce qui la confirmerait | Statut |
|---|---|---|---|---|---|---|
| H-1 | À semaine identique, le gazole est plus cher dans les stations d'autoroute que hors autoroute. | QA-3.1 | Écart hebdomadaire entre le prix médian autoroute et le prix médian hors autoroute, en cts/L et en % (base : `prix_hebdo_par_station`) | Pour chaque semaine, médiane des stations A moins médiane des stations R ; on compte les semaines où l'écart est positif et on indique les effectifs A et R ; stations `pop = N` exclues (ANO-14) | Écart médian positif sur la grande majorité des semaines, avec le nombre de stations indiqué | **Confirmée** (#41) : écart A moins R positif sur 153 semaines sur 157 (97,5 %), médiane +8,8 cts/L (+4,9 %, soit 8,8 € pour 100 L), avec 26 à 39 stations A et 430 à 784 stations R par semaine. À département égal, écart positif dans les 4 départements comptant au moins 5 stations A (77, 78, 91, 95 : de +9,1 à +12,2 cts/L, D-19).<br>Limites : 4 semaines négatives consécutives en octobre 2022 ; écart plus faible aux T3 et T4 2022 (+3,5 et +1,05 cts/L) ; première semaine partielle. |
| H-2 | Le prix médian du gazole est plus élevé à Paris (75) que dans les départements de grande couronne. | QA-1.1 | Prix médian par département (médiane des médianes par station), écart au 75 en cts/L et en % (`prix_median_par_departement`, D-13) | Comparaison du prix médian du 75 avec celui de chaque département 77, 78, 91, 95, en indiquant le nombre de stations par département ; calcul fait année par année (2021, 2022, 2023) | Prix médian du 75 supérieur à celui des départements 77, 78, 91 et 95 | Confirmée |
| H-3 | Les prix publiés en 2022 intègrent la remise à la pompe. | QA-4.1, QA-4.3 | Prix médian hebdomadaire de la région, en €/L (`prix_median_hebdo`) | Variation du prix médian entre la semaine qui précède et celle qui suit chaque changement de remise (entrée en vigueur, changements de montant, fin), comparée au montant officiel de la remise ; on indique le nombre de stations chaque semaine | Baisse nette du prix médian hebdomadaire aux dates d'entrée en vigueur de la remise, et hausse à sa sortie, d'un ordre de grandeur comparable au montant officiel | Formulée |
| H-4 | Chaque année, le gazole est plus cher en juillet et en août que sur l'ensemble de l'année. | QA-2.1, QA-2.2 | Écart entre le prix médian du mois et le prix médian de son année, en cts/L, en % et en € pour 100 L (D-09) ; base : prix moyen mensuel par station, puis médiane des stations | Pour 2021, 2022 et 2023, on lit l'écart de juillet et d'août, on compte les années où les deux écarts sont positifs et on indique le nombre de stations par mois ; une tendance au sein de l'année (hausse continue, mesures de 2022 vues en H-3) peut créer un écart sans lien avec la saison, ce qui est signalé comme limite | Écarts de juillet et d'août positifs sur les trois années | Infirmée (2026-11-19, #44) : juillet au-dessus de la médiane de son année 1 fois sur 3, août 2 fois sur 3 ; les écarts suivent surtout l'évolution propre à chaque année
=======
| ID  | Hypothèse                                                                                          | Sous-question  | Indicateur                                                                                                                             | Méthode de comparaison descriptive                                                                                                                                                                                                                | Ce qui la confirmerait                                                                                                                                            | Statut    |
| --- | -------------------------------------------------------------------------------------------------- | -------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| H-1 | À semaine identique, le gazole est plus cher dans les stations d'autoroute que hors autoroute.     | QA-3.1         | Écart hebdomadaire entre le prix médian autoroute et le prix médian hors autoroute, en cts/L et en % (base : `prix_hebdo_par_station`) | Pour chaque semaine, médiane des stations A moins médiane des stations R ; on compte les semaines où l'écart est positif et on indique les effectifs A et R ; stations `pop = N` exclues (ANO-14)                                                 | Écart médian positif sur la grande majorité des semaines, avec le nombre de stations indiqué                                                                      | Formulée  |
| H-2 | Le prix médian du gazole est plus élevé à Paris (75) que dans les départements de grande couronne. | QA-1.1         | Prix médian par département (médiane des médianes par station), écart au 75 en cts/L et en % (`prix_median_par_departement`, D-13)     | Comparaison du prix médian du 75 avec celui de chaque département 77, 78, 91, 95, en indiquant le nombre de stations par département ; calcul fait année par année (2021, 2022, 2023)                                                             | Prix médian du 75 supérieur à celui des départements 77, 78, 91 et 95                                                                                             | Confirmée |
| H-3 | Les prix publiés en 2022 intègrent la remise à la pompe.                                           | QA-4.1, QA-4.3 | Prix médian hebdomadaire de la région, en €/L (`prix_median_hebdo`)                                                                    | Variation du prix médian entre la semaine qui précède et celle qui suit chaque changement de remise (entrée en vigueur, changements de montant, fin), comparée au montant officiel de la remise ; on indique le nombre de stations chaque semaine | Baisse nette du prix médian hebdomadaire aux dates d'entrée en vigueur de la remise, et hausse à sa sortie, d'un ordre de grandeur comparable au montant officiel | Formulée  |

## 1 ter. Expression des écarts

Les écarts sont donnés en cts/L et en %, et aussi en euros pour un volume de référence (D-09) : écart en € = écart en cts/L × volume en litres / 100.

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

### Q-02 · Carburant retenu

- **Date de la question** : 2026-10-27
- **Posée par** : Noé Chauvin
- **Question** : quel carburant l'analyse doit-elle couvrir ?
- **Réponse** : le gazole.
- **Date de la réponse** : 2026-10-27 (échange oral, confirmé par écrit le 27/10/2026)
- **Conséquence** : D-06.

### Q-03 · Structure des questions analytiques

- **Date** : 2026-10-27
- **Posée par** : Noé Chauvin (présentation du brouillon v1)
- **Retour du commanditaire** : chaque axe principal doit être décomposé en 2 ou 3 sous-questions simples.
- **Date de la réponse** : 2026-10-27 (échange oral, confirmé par écrit le 27/10/2026)
- **Conséquence** : sous-questions QA-x.y dans la section 1.

### Q-04 · Chocs à analyser

- **Date de la question** : 2021-2023
- **Posée par** : Noé Chauvin
- **Question** : quels événements récents souhaitez-vous voir analysés (périodes ou dates précises) ?
- **Réponse** : partielle. Le commanditaire ne liste pas d'événements mais exige que chaque événement cité soit daté à partir d'une source officielle référencée (Q-05).
- **Conséquence** : l'équipe propose la liste des événements avec leurs sources ; la liste est soumise au commanditaire avec la synthèse.

### Q-05 · Validation du cadrage v1

- **Date de la question** : 2026-10-[jj] (envoi du document de cadrage v1)
- **Posée par** : Noé Chauvin
- **Réponse** : cadrage v1 validé sous réserves :
  - gazole et période 2021-2023 validés ; **région à confirmer avant le vendredi 30/10/2026** ;
  - QA-1.2 : préciser et justifier le seuil minimal de stations par commune → D-08 ;
  - QA-2.3 : peut rester exploratoire ;
  - QA-3 : indiquer le nombre de stations d'autoroute derrière chaque comparaison ;
  - QA-4.3 : dater chaque événement à partir d'une source officielle ; préciser si les prix publiés intègrent la remise à la pompe → H-3 ;
  - formuler au moins deux hypothèses avant calcul → section 1 bis ;
  - exprimer les écarts en euros pour un volume donné → D-09 ;
  - toute modification ultérieure des questions lui est soumise par écrit.
- **Date de la réponse** : 2026-10-28 (écrit)
- **Message archivé** :

Mohamed BENYAMINA<m.benyamina@intervenant-ggeedu.fr>

Noé CHAUVIN
Bonjour Noé,

Merci pour ce document clair et bien structuré. Le cadrage et les quatre axes répondent au besoin exprimé : je valide cette version 1, sous réserve des points suivants.
Gazole et période 2021 à 2023 : validés.
Région : merci de me la confirmer d'ici le vendredi 30/10. Sans région arrêtée, je ne peux pas considérer le cadrage comme définitif.

QA-1 (où)
Validé.
Pour 1.2, un classement de communes n'a de sens que si chaque commune compte assez de stations. Précisez le seuil minimal retenu et justifiez-le.
QA-2 (quand)
Validé.
La question 2.3 peut rester exploratoire : si les données ne permettent pas d'y répondre de manière fiable, expliquez pourquoi plutôt que de forcer un résultat.
QA-3 (autoroute)
Validé. C'est l'axe le plus attendu par nos adhérents.
Indiquez le nombre de stations d'autoroute sur lequel repose chaque comparaison, pour que l'on sache quel crédit accorder à l'écart.
QA-4 (évolution)
Validé.
Pour 4.3, chaque événement cité doit être daté à partir d'une source officielle référencée.
Précisez également si les prix publiés intègrent ou non la remise à la pompe : cela change la lecture de 2022.

Deux attentes complémentaires
Formulez au moins deux hypothèses avant tout calcul, puis indiquez si les données les confirment ou les infirment.
Pour que nos adhérents s'approprient les résultats, exprimez si possible les écarts trouvés en euros pour un volume de carburant donné, et pas seulement en centimes par litre.
Vous pouvez archiver ce message dans docs/questions.md. Toute modification ultérieure des questions devra de nouveau m'être soumise par écrit.

Bonne continuation à toute l'équipe.
Cordialement,
BENYAMINA Mohamed

### Q-06 · Format du flux v2

- **Date de la question** : 2026-10-28
- **Posée par** : Noé Chauvin
- **Question** : le flux v2 doit-il être utilisé au format XML (fichier du ministère) ou la version CSV de data.gouv.fr est-elle acceptée ? Par défaut, l'équipe annonçait le XML.
- **Réponse** : le XML n'est imposé que pour l'historique annuel. Pour le flux v2, les deux formats sont acceptés, à condition de justifier le choix dans `docs/decisions.md`. Le périmètre gazole, Île-de-France, 2021-2023 est validé.
- **Date de la réponse** : 2026-10-28 (écrit)
- **Conséquence** : réserve « région » de Q-05 levée ; choix du format → D-10.
