# 3 Gérer les risques liés à l'IA générative dans les tests

### Mots-clés

confidentialité des données, sécurité, vulnérabilité

### Termes de l’IA générative

Biais, erreur de raisonnement, hallucination, température

### Objectifs d'apprentissage et objectifs d'apprentissage pratique pour le chapitre 3 :

## 3.1 Hallucinations, erreurs de raisonnement et biais

- **GenAI-3.1.1 (K1) Rappeler les définitions des hallucinations , des erreurs de raisonnement et des biais dans les systèmes d'IA générative**
- **GenAI-3.1.2 (K3) Analyser les hallucinations, les erreurs de raisonnement et les biais dans les résultats des LLMs**
- **HO-3.1.2a (H1) Expérimenter les hallucinations lors de tests avec l'IA générative**
- **HO-3.1.2b (H1) Expérimenter les erreurs de raisonnement lors de tests avec l'IA générative**
- **GenAI-3.1.3 (K2) Résumer les techniques d'atténuation des hallucinations , des erreurs de raisonnement et des biais de l'IA générative dans les tâches de test logiciel**
- **GenAI-3.1.4 (K1) Rappeler les techniques d'atténuation pour le comportement non déterministe des LLMs**

## 3.2 Confidentialité des données et risques de sécurité liés à l'IA générative dans les tests logiciels

- **GenAI-3.2.1 (K2) Expliquer les principaux risques liés à la confidentialité des données et à la sécurité associés à l'utilisation de l'IA générative dans les tests logiciels**
- **GenAI-3.2.2 (K2) Donner des exemples de confidentialité des données et de vulnérabilités liées à l'utilisation de l'IA générative dans les tests logiciels**
- **GenAI-3.2.3 (K2) Résumer les stratégies d'atténuation visant à protéger la confidentialité des données et à renforcer la sécurité dans l'IA générative pour les tests logiciels**
- **HO-3.2.3 (H0) Reconnaître les risques liés à la confidentialité et à la sécurité des données dans une étude de cas de test avec l'IA générative**

## 3.3 Consommation énergétique et impact environnemental de l'IA générative pour les tests logiciels

- **GenAI-3.3.1 (K2) Expliquer l'impact des caractéristiques des tâches et de l'utilisation des modèles sur la consommation énergétique de l'IA générative dans les test logiciels**
- **HO-3.3.1 (H1) Utiliser un simulateur pour calculer l'énergie et les émissions de CO₂ pour des tâches de test données avec l'IA générative**

## 3.4 Règlements, normes et cadres de bonnes pratiques en matière d'IA

- **GenAI-3.4.1 (K1) Rappeler des exemples de réglementations, de normes et de cadres de bonnes pratiques en matière d'IA pertinents pour l'IA générative pour les tests logiciels**

## 3.1 Hallucinations, erreurs de raisonnement et biais

Les systèmes d'IA générative , en particulier les LLMs, sont sujets à certains défauts, notamment des
hallucinations, des erreurs de raisonnement et des biais. Ces défauts réduisent la qualité des résultats de
l'IA générative lors des tâches de test, ce qui se traduit par la génération de testware qui ne répond pas
aux attentes des testeurs. Ces hallucinations, erreurs de raisonnement et biais doivent être iden tifiés par
les testeurs dans les résultats des LLMs, et des mesures doivent être prises pour atténuer ces risques .
Le comportement non déterministe des LLMs (voir section 1.1.2) rend difficile la correction de ce type de
défauts ; ceux -ci peuvent sembler être corrigés pour une sortie générée par un LLM, mais réapparaître
dans une autre conversation avec ce même LLM.

### 3.1.1 Hallucinations, erreurs de raisonnement et biais dans l'IA générative

Les hallucinations se produisent lorsqu'un LLM génère une sortie qui se révèle factuellement incorrecte
ou non pertinente pour une tâche donnée. Dans les tests logiciels, les hallucinations produites par les LLMs
peuvent se manifester sous forme de cas de test fictifs ou non pertinents , de la génération de scripts de
test incorrects ou non fonctionnels, ou de la suggestion de cas de test qui vérifient des critères d'acceptation
inexistants. Cela peut induire les testeurs en erreur et compromettre la validité des résultats des tests .
Les erreurs de raisonnement se produisent lorsque les LLMs interprètent mal les structures logiques,
telles que les relations de cause à effet, la logique conditionnelle ou les processus de résolution de
problèmes étape par étape ; ce qui conduit à des conclusions incorrectes. Contrairement aux humains, les
LLMs ne disposent pas d'un véritable raisonnement logique et s'appuient sur la reconnaissance de motifs,
ce qui peut conduire à des erreurs logiques lors de l'exécution de tâches telles que le raisonnement
mathématique (Mirzadeh 2 024). La planification des tests et la hiérarchisation des cas de test sont des
exemples de tâches de test qui nécessitent un raisonnement logique et où les LLMs peuvent commettre
des erreurs de raisonnement.
Les biais des LLMs (Gallegos 2024) proviennent des données sur lesquelles le modèle a été entraîné.
Ces biais peuvent conduire à des résultats qui favorisent certains types d'informations, d'approches ou
d'hypothèses. Par exemple, les LLMs entraînés principalement sur des données en anglais peuvent sous-
représenter les perspectives non anglophones. Dans les tests logiciels, les biais peuvent influencer les
réponses des LLMs, par exemple lors de la génération de données de test ou du remaniement des critères
d'acceptation pour les cas de test.
Les hallucinations, les erreurs de raisonnement et les biais dans les résultats de l'IA générative résultent
de la nature des données d'entraînement et des limites inhérentes au modèle Transformer (voir chapitre
1). Reconnaître et surmonter ces problèmes permet d'améliorer la qualité des résultats de l'IA générative
dans les processus de test.

### 3.1.2 Identifier les hallucinations, les erreurs de raisonnement et les biais dans les résultats des LLMs

L'intégration efficace des systèmes d'IA générative dans les tests logiciels nécessite la capacité de détecter
les hallucinations, les erreurs de raisonnement et les biais dans les résultats fournis par les LLMs. Selon le
type de problème, différentes approches de détection peuvent être appliquées. Voici les approches
courantes qui sont appliquées au moyen d'une revue humaine ou d'une combinaison de revue humaine et
de vérification automatisée :
Détection des hallucinations :

- Vérification croisée : comparer les résultats générés par l'IA avec la documentation existante, les
  exigences et le comportement connu du système. Des outils automatisés peuvent aider à recouper
  les résultats avec des sources de données établies afin de signaler les divergences .
- Consultation d'experts dans le domaine : faites appel à des experts pour valider l'exactitude du
  contenu généré. Leur expertise est essentielle pour saisir les nuances que les systèmes
  automatisés pourraient négliger.
- Contrôles de cohérence : vérifier que les résultats générés sont cohérents entre eux et avec les
  informations connues. Les systèmes automatisés peuvent aider à identifier les motifs d'erreurs et
  à signaler les incohérences.
  Détection d'erreurs de raisonnement :
- Validation logique : Évaluer le flux logique (par exemple, la cohérence, la cohésion et le
  raisonnement structuré dans le texte généré) du contenu généré par l'IA afin d'en vérifier la
  cohérence et l'exactitude au moyen de cycles de revue. Des outils automatisés peuvent être utiles,
  mais les cas complexes peuvent nécessiter un jugement humain.
- Test des résultats : par exemple, exécution des cas de test ou des scripts de test générés sur les
  objets de test afin de vérifier les résultats du test. Cette opération peut être partiellement ou
  entièrement automatisée, selon le type de testware généré.
  Détection de biais :
- Revoir comment les testware générés, tels que les données de test synthétiques, sont représentés
  de manière équitable et précise par rapport à la stratégie de test.
  Évaluer les biais liés aux types de tests, tels que la sous -représentation des tests non fonctionnels
  dans les résultats générés par le LLM . L'implémentation effective de ces méthodes de détection
  dépendra du niveau de risque estimé d'hallucinations , d'erreurs de raisonnement ou de biais dans la
  tâche de test effectuée avec l'IA générative.

Objectif d'apprentissage pratique 3.1.2a (H1) : Expérimenter les hallucinations de l'IA générative
liées à une tâche de test logiciel
Cet exercice se concentre sur l'expérimentation d'exemples d'hallucinations de l'IA générative en relation
avec l'ensemble des connaissances en matière de test logiciel. Les participants confrontent au moins
deux LLMs à une situation dans laquelle les LLMs inventent des éléments non pertinents, par exemple
en ajoutant des critères sans rapport qui n'existent pas dans les données contextuelles fournies.
Différents prompts sont testés afin d'examiner leur influence sur les hallucinations.

Cet exercice permet de mieux comprendre comment identifier les hallucinations de l'IA générative lors
des tests logiciels.

Objectif d'apprentissage pratique 3.1.2b (H1) : Expérimenter les erreurs de raisonnement de l'IA
générative dans une tâche de planification des tests
Cet exercice vise à présenter un exemple d'erreur de raisonnement de l'IA générative . Il s'agit d'un
exemple de problème à résoudre dans le domaine de la planification des tests, tel que l'estimation de
l'effort de test et la hiérarchisation des cas de test (voir [ISTQB_CTFL] - Chapitre 5). L'exercice est conçu
avec une certaine complexité des données d'entrée, ce qui nécessite des compétences en résolution de
problèmes et met en évidence les limites des LLMs pour cet objectif. Le résultat du LLM sera comparé
au résultat exact qui devrait être obtenu. Trois types de LLM différents seront essayés (LLM, SLM et
modèle de raisonnement), et des variations du prompt seront utilisées pour tenter d'améliorer les
résultats.
Cet exercice permet de mieux comprendre comment identifier les erreurs de raisonnement de l'IA
générative dans les tâches de test logiciel qui nécessitent des compétences en résolution de problèmes
logiques.

### 3.1.3 Techniques d'atténuation des hallucinations, des erreurs de raisonnement et des biais de l'IA générative dans les tâches de test logiciel

Afin de minimiser les résultats non souhaités de l'IA générative dans les tests logiciels, plusieurs stratégies
peuvent être employées pour réduire les hallucinations , les erreurs de raisonnement et les biais . Ces
problèmes sont plus susceptibles de se produire lorsque les prompts ne sont pas correctement conçus
(voir chapitre 2) ou lorsque les données d'entrée contextuelles pertinentes font défaut pour une tâche de
test donnée. Les techniques clés pour atténuer les risques associés aux hallucinations, aux erreurs de
raisonnement et aux biais de l'IA comprennent :

- Fournir un contexte complet : veiller à ce que le prompt contienne toutes les informations
  pertinentes (voir section 2.1.1), en offrant un contexte complet pour guider l'IA dans la production
  de résultats précis.
- Diviser les prompts en segments gérables : divise r les prompts complexes en étapes plus
  petites à l'aide de techniques d'enchaînement de prompts (voir section 2.1.2), en vérifiant
  systématiquement chaque sortie avant de passer à la suivante. Cette approche étape par étape
  peut aider à la détection d`erreurs de raisonnement dès le début du processus de génération.
- Utiliser des formats de données clairs et interprétables : éviter les formats qui peuvent être
  ambigus ou difficiles à interpréter pour l'IA générative . Des formats structurés et simples aident le
  modèle à se concentrer sur les aspects essentiels de la tâche.
- Sélectionner le modèle d'IA générative approprié à la tâche : utiliser un LLM spécialement
  entraîné pour la tâche à accomplir (voir section 5.1.3).

- Comparer les résultats entre les modèles : lorsque cela est approprié, évaluer le prompt avec
  plusieurs LLMs et comparer les résultats permet de détecter les erreurs et de sélectionner les
  résultats les plus fiables.
  Le chapitre 4 présente deux techniques complémentaires permettant d'améliorer les résultats du LLM : la
  génération augmentée par la recherche (Retrieval-Augmented Generation) et le réglage fin (Fine-Tuning).

### 3.1.4 Atténuation du comportement non déterministe des LLMs

Le comportement non déterministe inhérent aux LLMs (Shuyin 2023) peut entraîner des variations dans
les résultats, même lorsque la même entrée est fournie. Cela résulte des processus d'échantillonnage
probabilistes utilisés lors de l'inférence. Par conséquent, il peut être difficile d'obtenir des résultats
cohérents et reproductibles lors de l'utilisation des LLMs, en particulier pour les résultats longs, ce qui
augmente le risque de variabilité.
Bien qu'il soit impossible de garantir une reproductibilité totale, certaines stratégies peuvent contribuer à
réduire la variabilité :

- Ajuster les paramètres de température du LLM : abaisser la température pendant la génération
  de réponses (inférence) réduit la distribution de probabilité, ce qui diminue le caractère aléatoire et
  permet d'obtenir des résultats plus cohérents. Cependant, cela limite également la créativité et la
  diversité des réponses, rendant les résultats plus répétitifs ou trop déterministes .
- Définition de graines aléatoires (NDT : random seeds) : certaines implémentations LLM
  permettent de définir une valeur de graine pour le générateur de nombres aléatoires, garantissant
  ainsi l'utilisation de la même séquence pseudo -aléatoire (c'est -à-dire des valeurs aléatoires
  déterministes), ce qui améliore la reproductibilité.
  Réduire le risque d'hallucinations et d'erreurs de raisonnement dans les résultats du LLM implique de
  remédier à ce comportement non déterministe, par exemple en automatisant certains aspects de la
  vérification des résultats de façon à mettre en place un processus d'évaluation structuré et cohérent .

## 3.2 Confidentialité des données et risques de sécurité liés à l'IA générative dans les tests logiciels

L'IA générative dans les tests introduit des risques liés à la confidentialité et à la sécurité des données en
raison du traitement d'informations sensibles et des vulnérabilités potentielles de l'infrastructure de test
alimentée par LLM . Une protection robuste des données est essentielle pour prévenir les violations, les
accès non autorisés et l'exposition de données confidentielles.

### 3.2.1 Confidentialité des données et risques de sécurité liés à l'utilisation de l'IA générative

L'IA générative peut traiter de grandes quantités de données susceptibles de contenir des informations
sensibles ou personnelles. Cela soulève les questions suivantes sur la confidentialité des données :

- Exposition involontaire des données : les modèles d'IA générative peuvent générer des
  résultats qui révèlent accidentellement des informations sensibles.

- Manque de contrôle sur l'utilisation des données : les outils d'IA générative peuvent stocker et
  traiter des données sensibles sans le consentement explicite ou le contrôle de l'utilisateur. Cela
  peut entraîner une utilisation abusive ou un accès non autorisé.
- Risques liés à la conformité : l'utilisation d'outils d'IA générative sans respecter les
  réglementations en matière de protection des données, telles que le règlement général sur la
  protection des données (RGPD, règlement (UE) 2016/679), pourrait entraîner des litiges juridiques.
  De plus, des risques de sécurité spécifiques apparaissent lors des tests avec l'IA générative, tels que :
- Les infrastructures de test basées sur les LLMs peuvent être vulnérables aux attaques de sécurité,
  telles que les violations de données ou les accès non autorisés.
- Les acteurs malveillants peuvent exploiter les vulnérabilités des LLMs, comme les attaques
  manipulatrices (voir section 3.2.2), pour modifier leur comportement ou extraire des informations
  sensibles.
- Les attaquants peuvent introduire intentionnellement des données d'entrée malveillantes afin de
  tromper les LLMs et compromettre leur précision ou leur sécurité.

### 3.2.2 Confidentialité des données et vulnérabilités dans l'IA générative pourles processus et outils de tests

Le tableau suivant donne quelques exemples de vecteurs d'attaque dans les processus et outils de test de l'IA générative.
| **Vecteur d'attaque** | **Description** | **Exemple** |
|---|---|---|
| _Exfiltration de données_ | Prompts conçus pour extraire des données confidentielles d'entraînement. | Dépasser la fenêtre contextuelle du LLM avec de longs prompts afin de surcharger la mémoire de l'IA pourrait l'amener à révéler des extraits aléatoires de ses données d'entraînement et potentiellement exposer des informations sensibles. |
| _Manipulation des prompts_ | Introduction de données qui perturbent les résultats de l'IA. | Images qui induisent l'IA dans un contexte différent, provoquant ainsi des hallucinations, par exemple sur les critères d'acceptation. |
| _Contamination des données_ | Manipulation des données d'entraînement. | Fournir de fausses évaluations lors de la notation des résultats d'un rapport de test généré par l'IA. |
| _Génération de code malveillant_ | Manipulation d'un LLM pour générer des portes dérobées (par exemple, des appels de commandes externes) pendant l'utilisation. | Génération de code pour ouvrir un canal de communication avec une adresse IP malveillante spécifique. |

### 3.2.3 Stratégies d'atténuation pour protéger la confidentialité des données et renforcer la sécurité lors des tests avec l'IA générative

À mesure que l'IA générative se généralise, et compte tenu des risques inhérents, des réglementations et
des normes apparaissent pour les atténuer (voir section 3.4.1).
Les réglementations en matière de protection des données telles que le RGPD ne restreignent pas
explicitement les applications de l'IA générative, mais prévoient des garanties susceptibles de limiter ce qui
peut être fait, notamment en ce qui concerne la légalité et les restrictions relatives aux finalités de la
collecte, du traitement et du stockage des données.
Pour atténuer ces risques, les organisations doivent mettre en œuvre des mesures robustes de
confidentialité des données, notamment :

- Minimisation des données : éviter le traitement des données sensibles sauf si la loi l'autorise et
  n'utiliser que la quantité nécessaire de données non sensibles lors des tests avec l'IA afin de
  réduire les risques liés à la confidentialité des données.
- Anonymisation et pseudonymisation des données : masquage ou remplacement des
  informations sensibles par des données non identifiables.
- Stockage et transmission sécurisés des données : implémentation d'un cryptage puissant et
  de contrôles d'accès.
- Formation du personnel : les organisations doivent mettre en place des programmes et des
  politiques de formation clairs afin de garantir une utilisation responsable des outils d'IA générative,
  de promouvoir des pratiques éthiques et d'atténuer les risques potentiels .
  Des stratégies d'atténuation supplémentaires peuvent être envisagées lors de l'implémentation de l'IA
  générative pour les tests :
- Revue systématique des résultats générés : l'évaluation humaine est essentielle pour garantir
  la qualité et la précision des tâches de test basées sur l'IA générative.
- Évaluation par comparaison avec un autre LLM : cette méthode consiste à utiliser plusieurs
  LLMs sur une tâche donnée afin d'évaluer les résultats en comparant leurs réponses .
- Choix d'un environnement sécurisé et opérationnel : en fonction du niveau de confidentialité
  requis, les organisations peuvent opter pour différentes solutions sécurisées : utilisation d'une offre
  commerciale sécurisée proposée par un fournisseur LLM , exploitation du LLM dans un cloud
  sécurisé ou installation du LLM dans l'infrastructure de l'organisation.
- Audits de sécurité et évaluations des vulnérabilités réguliers : identification et correction des
  faiblesses des systèmes d'IA générative.
- Rester informé des meilleures pratiques en matière de sécurité : se tenir au courant des
  dernières directives et technologies en matière de sécurité.
  Ces stratégies sont souvent complémentaires et leur combinaison est nécessaire pour garantir la sécurité
  des données lors de l'utilisation de l'IA générative. Il est fortement recommandé d'impliquer des ingénieurs
  en sécurité expérimentés, des conseillers juridiques, le directeur technique (CTO) ou le responsable de la
  sécurité des systèmes d'information (CISO), s'ils sont présents dans l'organisation .

## 3.3 Consommation énergétique et impact environnemental de l'IA générative dans les tests logiciels

Des études telles que (Luccioni 2024a) montrent que l'entrainement et l'utilisation des LLMs nécessitent la
mise en œuvre intensive d'un grand nombre de ressources informatiques spécialisées. Les LLMs sont mis
à disposition sous forme de services Web, et leur utilisation augmente la charge sur les appareils, les
réseaux et les centres de données, ce qui entraîne une consommation d'énergie plus élevée.

### 3.3.1 L'impact de l'utilisation de l'IA générative sur la consommation d'énergie et les émissions de CO2

L'impact environnemental de l'IA générative ne doit pas être sous -estimé, car la consommation d'énergie
augmente fortement avec l'utilisation. La complexité de la tâche et les ressources informatiques
nécessaires influencent la consommation d'énergie. Par exemple, la génération d'une seule image à l'aide
d'un modèle d'IA puissant peut consommer autant d'énergie que la recharge complète d'un smartphone,
tandis que la génération de texte ne consomme qu'un faible pourcentage de la charge d'un smartphone
(Heikkilä 2023).
Même s'il est difficile d'obtenir des données précises sur l'impact environnemental de l'IA générative
(Luccioni 2024b), il est clair que ces opérations énergivores contribuent collectivement à des émissions de
CO₂ importantes (Berthelot 2024). Si une seule recherche ou une seule tâche de génération de texte peut
sembler n égligeable, leur effet cumul é sur des millions d'utilisateurs à travers le monde entra îne une
pression environnementale considérable.
L'adoption de bonnes pratiques, telles que la limitation des interactions inutiles avec les modèles, est
essentielle pour atténuer les risques environnementaux posés par l'IA générative .

Objectif d'apprentissage pratique 3.2.3 (H0) : Reconnaître les risques liés à la confidentialité
et à la sécurité des données dans une étude de cas donnée sur tester avec l'IA générative
Cette démonstration illustre comment des risques liés à la confidentialité et à la sécurité des
données peuvent survenir lors de l'utilisation de l'IA générative dans les tests logiciels. Les
participants exploreront des études de cas afin d'identifier les menaces potentielles, telles que les
vulnérabilités des modèles, l'accès non autorisé aux données ou l'utilisation malveillante des
résultats générés. Ils exploreront des stratégies d'atténuation, notamment le traitement sécurisé des
données, les contrôles d'accès robustes et les pratiques de surveillance de l'IA, tout en réfléchissant
aux implications éthiques et pratiques.
À la fin, les participants comprendront les principes de confidentialité des données et apprendront
à reconnaître et à traiter les risques de sécurité dans les conditions de test de l'IA générative.

Objectif d'apprentissage pratique 3.3.1 (H1) : Utiliser un simulateur pour calculer l'énergie et les
émissions de CO₂ pour des tâches de test données avec l'IA générative.
Cet exercice se concentre sur l'évaluation de la consommation d'énergie et des émissions de CO ₂
associées à diverses t âches d'IA g énérative dans le domaine des tests logiciels. Les participants
utiliseront des simulations pour calculer ces m étriques et examiner comment les diff érentes
caractéristiques des tâches et l'utilisation des LLMs affectent l'impact environnemental.
En observant comment différents facteurs influencent la consommation d'énergie et les émissions, les
participants comprennent les principaux facteurs de consommation d'énergie avec les LLMs .

## 3.4 Réglementations, normes et cadres de bonnes pratiques en matière d'IA

L'IA générative transforme les tests logiciels en aidant les testeurs dans diverses tâches de test (voir
chapitre 2). Cependant, ces opportunités s'accompagnent également de risques importants, tels que les
erreurs de raisonnement, la confidentialité des données, les vulnérabilités et les impacts environnementaux
(voir sections 3.1, 3.2 et 3.3). Pour faire face à ces risques, il convient de tenir compte des réglementations
générales, des normes et des cadres de bonnes pratiques en matière d'IA.

### 3.4.1 Réglementations, normes et cadres relatifs à l'IA générative dans le domaine des tests logiciels

Le tableau ci-dessous donne une vue d'ensemble des principales directives relatives à l'utilisation de l'IA
générative dans les tests logiciels :

| **Nom / Type**                                                                                                                    | **Description**                                                                                                                        | **Application dans les tests logiciels**                                                                                                   |
| --------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| _ISO/IEC 42001:2023_<br>Technologies de l'information – Intelligence artificielle – Système de management<br><br>Type: Norme      | Spécifie les exigences relatives à la gestion des systèmes d'IA au sein d'une organisation.                                            | Garantit que l'IA générative utilisée lors des tests respecte les pratiques recommandées, favorisant ainsi la cohérence et la fiabilité.   |
| _ISO/IEC 23053:2022_<br>Cadre pour les systèmes d'intelligence artificielle (IA) utilisant le machine learning<br><br>Type: Norme | Fournit un cadre pour les processus du cycle de vie de l'IA, en mettant l'accent sur la sûreté et la transparence.                     | Fournit un cadre pour la qualité des données, la transparence et la sûreté lors de l'utilisation de l'IA générative pour tester.           |
| _EU AI Act_<br><br>Type: Réglementation<br>Source: (AI Act 2024)                                                                  | Établit un cadre juridique traitant des risques liés à l'IA, classant les applications par niveau de risque.                           | Exige la conformité en matière de transparence, de responsabilité et d'atténuation des biais pour l'IA générative utilisée dans les tests. |
| _NIST AI Risk Management Framework (US)_<br><br>Type: Framework<br>Source: (NIST AI RMF 1.0)                                      | Propose des recommandations pour la gestion des risques liés à l'IA, en mettant l'accent sur l'équité, la transparence et la sécurité. | Garantit l'équité et atténue les risques liés à l'IA générative, afin d'éviter les résultats de test biaisés.                              |

À mesure que les technologies d'IA et leur cadre réglementaire continuent d'évoluer, il est impératif pour
les organismes de test de se tenir informés des développements en matière de réglementations, de
normes, de lois nationales et de cadres de bonnes pratiques, tels que ceux présentés dans ce tableau.
