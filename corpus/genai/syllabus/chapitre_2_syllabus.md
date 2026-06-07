# 2 Ingénierie du prompting pour des tests logiciels efficaces

### Mots-clés

cas de test, condition de test, critères d'acceptation, données de test, conception de test, rapport de test,
script de test

### Termes de l’IA générative

enchaînement de prompts, few-shot prompting, ingénierie du prompting, méta-prompting, one-shot
prompting, prompt, prompt système, prompt utilisateur, traitement du langage naturel, zero-shot
prompting

### Objectifs d'apprentissage et objectifs d'apprentissage pratique pour le chapitre 2 :

## 2.1 Développement efficace des prompts

- **GenAI-2.1.1 (K2) Donner des exemples de la structure des prompts utilisées dans l'IA générative pour les tests logiciels**
- **HO-2.1.1 (H0) Observer plusieurs prompts donnés pour des tâches de test logiciel, en identifiant les composants du rôle, du contexte, de l'instruction, des données d'entrée, des contraintes et du format de sortie dans chacune d'eux**
- **GenAI-2.1.2 (K2) Différencier les principales techniques de prompting pour les tests logiciels**
- **HO-2.1.2a (H0) Observer des démonstrations d'enchaînement de prompts, de few -shot prompting et de méta-prompting appliqués à des tâches de test logiciel**
- **HO-2.1.2b (H1) Identifier les techniques d'ingénierie du prompting utilisées dans des exemples donnés**
- **GenAI-2.1.3 (K2) Distinguer les prompts système des prompts utilisateur**

## 2.2 Application des techniques d'ingénierie du prompting aux tâches de test logiciel

- **GenAI-2.2.1 (K3) Appliquer l'IA générative aux tâches d'analyse de test**
- **HO-2.2.1a (H2) Pratiquer les prompts multimodaux pour générer des critères d'acceptation pour une User Story basée sur un maquette IHM**
- **HO-2.2.1b (H2) Pratiquer l'enchaînement de prompts et la vérification humaine pour analyser progressivement une User Story donnée et affiner les critères d'acceptation**
- **GenAI-2.2.2 (K3) Appliquer l'IA générative à la conception des tests et à l'implémentation des tests**
- **HO-2.2.2a (H2) Pratiquer la génération de cas de test fonctionnel à partir de User Stories avec l'IA générative en utilisant l'enchaînement de prompts, les prompts structurés et les méta-prompts**
- **HO-2.2.2b (H2) Utiliser la technique du few -shot prompting pour générer des conditions de test et des cas de test de style Gherkin à partir de User Stories**
- **HO-2.2.2c (H2) Utiliser l'enchaînement de prompts pour prioriser les cas de test dans une suite de tests donnée, en tenant compte de leurs priorités et dépendances spécifiques**
- **GenAI-2.2.3 (K3) Appliquer l'IA générative aux tests de régression automatisés**
- **HO-2.2.3a (H2) Pratiquer le few-shot prompting pour créer et gérer des scripts de test dirigés par les mots-clés**
- **HO-2.2.3b (H2) Pratiquer l'ingénierie du prompting structuré pour l'analyse des rapports de test dans le contexte des tests de régression**
- **GenAI-2.2.4 (K3) Appliquer l'IA générative aux tâches de contrôle et de suivi des tests**
- **HO-2.2.4 (H0) Observer les métriques de suivi des tests préparées par l'IA générative à partir des données de test**
- **GenAI-2.2.5 (K3) Sélectionner et appliquer les techniques de prompts appropriées à un contexte et à une tâche de test donnés**
- **HO-2.2.5 (H1) Sélectionner et appliquer des techniques de prompting adaptées au contexte pour une tâche de test donnée**

## 2.3 Évaluer les résultats de l'IA générative et affiner les requêtes pour les tâches de test logiciel

- **GenAI-2.3.1 (K2) Comprendre les métriques permettant d'évaluer les résultats de l'IA générative sur des tâches de test**
- **HO-2.3.1 (H0) Observer comment les métriques peuvent être utilisées pour évaluer le résultat de l'IA générative sur une tâche test**
- **GenAI-2.3.2 (K2) Donner des exemples de techniques permettant d'évaluer et de remanier de manière itérative les prompts.**
- **HO-2.3.2 (H1) Évaluer et optimiser un prompt pour une tâche de test donnée**

## 2.1 Développement efficace des prompts

Une conception efficace des prompts facilite la réalisation précise et efficace des tâches de test logiciel par
les outils d'IA générative, et que les testeurs obtiennent des résultats utiles des LLMs. Un prompt structuré
comprend différents composants (voir section 2.1.1). Chacun de ces composants contribue à la clarté et à
la précision d'un prompt qui communique efficacement les exigences et les attentes aux LLMs.
Diverses techniques d'ingénierie du prompting améliorent l'efficacité des prompts dans les tests logiciels.
Des techniques telles que l'enchaînement de prompts, le few -shot prompting et le méta -prompting
permettent de répondre à des sujets complexes en matière de tests (voir section 2.1.2) .
La combinaison de prompts structurés (voir section 2.1.1) et des techniques de prompt majeures vise à
obtenir de bons résultats lors de l'interrogation d'un LLM pour des tâches de test logiciel (voir section 2.1.3).

### 2.1.1 Structure des prompts pour l'IA générative dans les tests logiciels

Un prompt structuré pour le test logiciel comprend généralement six composants :

- Rôle : le rôle définit la perspective ou le persona que le modèle d'IA générative doit adopter lorsqu'il
  génère une réponse. La spécification du rôle aide le LLM à déterminer ses responsabilités et à
  adopter un ton ou une approche appropriés, par exemple en agissant comme un testeur, un test
  manager ou un ingénieur en automatisation des tests.
- Contexte : le contexte fournit les informations de base dont le modèle d'IA générative a besoin
  pour déterminer les conditions de test. Cela comprend des détails sur l'objet de test, la
  fonctionnalité spécifique à tester et toute information contextuelle pertinente.
- Instructions : les instructions sont des directives données à l'IA générative qui décrivent la tâche
  spécifique à effectuer. Des instructions claires, impératives et concises comprennent une
  description de la tâche et toutes les exigences pertinentes pour celle-ci.
- Données d'entrée : les données d'entrée comprennent toutes les informations nécessaires à
  l'exécution de la tâche, telles que les User Stories, les critères d'acceptation, les captures d'écran,
  le code, les cas de test existants ou les exemples de sortie. Fournir des données d'entrée détaillées
  et structurées aide le LLM à générer des résultats plus précis et plus adaptés au contexte.
- Contraintes : les contraintes décrivent les restrictions ou les considérations particulières
  auxquelles le LLM doit se conformer. Les contraintes aident à préciser comment les instructions
  doivent être appliquées aux données d'entrée.
- Format de sortie : les spécifications de sortie indiquent le format, la structure ou les
  caractéristiques attendus de la réponse. Cela aide à façonner la sortie du LLM .
  Ces composants forment la structure de base du prompt. Cette structure doit être combinée avec
  l'implémentation de techniques de prompting (voir section 2.1.2), en fonction de la tâche à accomplir et du
  LLM à utiliser.

Objectif d'apprentissage pratique HO-2.1.1 (H0) : Observer et analyser les composants du prompt
Dans une démonstration, plusieurs prompts structurés sont testées sur un chatbot IA , chacune étant
adaptée à des tâches spécifiques de test logiciel. Ces prompts suivent un format structuré composé de
six composants clés : rôle, contexte, instruction, données d'entrée, contraintes et format de sortie. La
démonstration vise à faciliter l'observation et l'analyse de ces prompts structurés, en mettant en évidence
la manière dont chaque composant contribue à fournir des informations précises, pertinentes et
exploitables à un LLM utilisé pour une tâche de test logiciel.

### 2.1.2 Principales techniques de prompting pour les tests logiciels

Ces dernières années, de nombreuses techniques de prompting LLM ont été proposées pour différents
cas d'utilisation de l'IA générative (Schulhoff 2024). Parmi celles -ci, trois techniques de prompting
principales sont couramment utilisées pour les tâches de test avec l'IA générative en conjonction avec la
structure de prompt à 6 composants décrite ci-dessus (voir section 2.1.1) : l'enchaînement de prompts, le
few-shot prompting et le méta-prompting.

- L'enchaînement de prompts consiste à diviser une tâche en une série d'étapes intermédiaires
  (plusieurs prompts). Le résultat de chaque étape est vérifié manuellement ou automatiquement et
  remanié avant de passer à l'étape suivante. Cette approche permet d'obtenir une plus grande
  précision, car chaque réponse informe le prompt suivant. L'enchaînement de prompts est
  particulièrement utile dans les processus de test où les tâches sont complexes et nécessitent une
  décomposition en sous -tâches et une vérification systématique des résultats intermédiaires du
  LLM. Il permet également des interactions dynamiques dans les processus de test .
- Le few-shot prompting consiste à fournir au LLM des exemples dans le prompt. Alors que le zero-
  shot prompting (sans exemple) s'appuie sur les connaissances préexistantes du modèle pour
  générer une réponse, le one -shot prompting fournit un exemple pour illustrer le résultat souhaité
  pour une entrée donnée. Les prompts avec la technique few-shot prompting contiennent plusieurs
  exemples (quelques-uns) afin de consolider davantage le comportement souhaité du modèle en
  matière de réponse.
  Cette technique aide à guider le modèle en fournissant une référence claire et en garantissant que
  les résultats sont cohérents et conformes aux attentes. Le few-shot prompting est particulièrement
  efficace pour les tâches où des exemples peuvent illustrer le comportement requis, permettant
  ainsi au modèle de généraliser efficacement et de produire des résultats fiables .
- Le méta-prompting exploite la capacité de l'IA à générer ou à remanier ses propres prompts.
  Dans un cycle itératif, le LLM peut générer des prompts qui peuvent être évalués et affinés par le
  testeur. Cette approche optimise la qualité des prompts en tirant parti des connaissances des LLMs
  en matière de prompts optimisés. Le méta-prompting est particulièrement utile lorsque l'efficience
  et l'optimisation des prompts sont essentielles, car elle réduit l'effort manuel nécessaire à la
  conception de prompts efficaces. Un autre avantage d u méta-prompting est que si le testeur ne
  sait pas comment créer un prompt efficace, il peut collaborer avec le LLM pour la co -créer. Cela
  reflète une forme de jumelage avec l'outil d'IA générative , où le testeur et l'IA travaillent ensemble
  de manière interactive pour atteindre un objectif commun. Ce concept de binôme met en avant une
  nouvelle façon de collaborer avec les outils d'IA, améliorant à la fois la productivité et

l'apprentissage, non seulement dans l'ingénierie du prompting, mais aussi dans la programmation
en binôme et les tests en binôme.
Ces techniques de prompt peuvent être utilisées efficacement en combinaison pour améliorer les résultats
du LLM (voir section 2.2.5).

Objectif d'apprentissage pratique HO-2.1.2a (H0): Observation et discussion de l'enchaînement
de prompts, du few-shot prompting et du méta-prompting dans des tâches de test logiciel
Les participants découvrent l'enchaînement de prompts, le few-shot prompting et le méta-prompting sur
un chatbot IA, chacun appliqué à des tâches spécifiques de test logiciel. La démonstration vise à explorer
et à discuter ces techniques de prompt dans le contexte des tests logiciels, en soulignant comment
chaque technique contribue à la précision et à l'exhaustivité des résultats du LLM .

Objectif d'apprentissage pratique HO-2.1.2b (H1): Identification de techniques d'ingénierie du
prompting à partir d'exemples donnés
Les participants lisent une série d'exemples de prompts liés aux tests logiciels afin d'identifier les
principales techniques de prompt utilisées. L'accent sera mis sur la reconnaissance de techniques telles
que l'enchaînement de prompts, le few -shot prompting et le méta -prompting, tout en soulignant leurs
caractéristiques distinctes et leurs applications pratiques.
Cette activité vise à approfondir la compréhension des participants sur la manière dont différentes
techniques de prompting améliorent l'utilisation efficace de l'IA générative dans les tests logiciels.

### 2.1.3 Prompt système et prompt utilisateur

Les prompts système et les prompts utilisateur ont des objectifs différents dans les interactions avec les
LLMs, chacun jouant un rôle distinct dans la formation de la conversation. Le prompt système est
généralement défini par le développeur ou le testeur afin de guider le comportement global du LLM. Il n'est
ni visible ni modifiable par l'utilisateur du chatbot dans la plupart des interfaces .
Un prompt système agit comme un ensemble de commandes prédéfinies qui définit le comportement, la
personnalité et les paramètres opérationnels du LLM . Les paramètres opérationnels déterminent la
manière dont le LLM répond, par exemple en utilisant un ton formel, en donnant des réponses concises,
en respectant les règles spécifiques au domaine ou en évitant certains comportements. Le prompt système
définit les règles pour l'ensemble de la conversation. Il peut contenir des parties d'un prompt structuré,
telles que le rôle, le contexte et les contraintes.
Le prompt système reste constant tout au long de la session d'interaction et établit le cadre de base de la
manière dont le LLM doit répondre. Par exemple, un prompt système peut dire : « Vous êtes un assistant
spécialisé dans les tests logiciels. Répondez toujours clairement, utilisez un langage formel et concentrez-
vous sur les pratiques recommandées par l'ISTQB®. Évitez les spéculations et citez les principes de test
lorsque cela est pertinent. »
Le prompt utilisateur, quant à lui, représente l'entrée ou la question réelle de l'utilisateur du chatbot. Il
change à chaque interaction et peut inclure des instructions spécifiques, des questions ou des tâches que
l'utilisateur du chatbot souhaite voir traiter par le LLM . Contrairement au prompt système , les prompts
utilisateur sont directement visibles et constituent le contexte immédiat de chaque réponse .
Par exemple, un prompt utilisateur pourrait être : « Enumère les principales différences entre les tests boîte
noire et boîte blanche à l'aide d'exemples. »
En général, le prompt système est défini une seule fois au début de la conversation, puis des prompts
utilisateur sont envoyés successivement pour chaque interaction. Le LLM génère des réponses en tenant
compte à la fois du prompt système, qui reste inchangé, et du prompt utilisateur actuel. Pour une
implémentation efficace, les prompts système doivent être clairs et précis quant au rôle du LLM et aux
contraintes éventuelles. Ils peuvent également contenir des informations contextuelles et des instructions
générales, par exemple concernant le résultat attendu.
Les prompts utilisateur doivent être ciblés et bien structurés, et inclure des instructions explicites ainsi que
des informations contextuelles supplémentaires pertinentes et des instructions relatives au format de sortie.

## 2.2 Application des techniques d'ingénierie du prompting aux tâches de test logiciel

L'application des techniques d'ingénierie du prompting aux tests logiciels permet à l'IA générative de
prendre en charge des tâches de test telles que l'analyse, la conception, l'automatisation, la hiérarchisation
des cas de test, la détection des défauts, l'analyse de la couverture, ainsi que la surveillance et le contrôle
des tests. En utilisant et en combinant des techniques telles que l'enchaînement de prompts, le few-shot
prompting et le méta-prompting, les équipes peuvent adapter les prompts de l'IA aux objectifs spécifiques
des tests, rendant ainsi les résultats plus précis, pertinents et efficaces. Des données d’entrée de haute
qualité sont essentielles pour obtenir des résultats significatifs avec l'IA générative.

### 2.2.1 Analyse de test avec l'IA générative

L'IA générative peut prendre en charge les tâches d'analyse de test en générant et en hiérarchisant les
conditions de test, en identifiant les défauts dans la base de test et en fournissant une analyse de
couverture. Les données d'entrée comprennent les exigences, les Us er Stories, les spécifications
techniques, les maquettes d'interface graphique et d'autres informations pertinentes. La sortie se compose
de produits de travail d'analyse de test typiques, tels que des conditions de test hiérarchisées (par exemple,
des critères d'acceptation).
Voici quelques tâches d'analyse de test typiques qui peuvent être prises en charge avec l'IA générative :

- Identifier les défauts potentiels dans la base de test : L'IA générative peut aider à analyser la
  base de test afin de détecter les incohérences, les ambiguïtés ou les informations incomplètes
  susceptibles d'entraîner des défauts. En comparant des motifs d'exigences similaires ou en
  appliquant les connaissances issues de rapports de défauts précédents, le LLM peut signaler les
  anomalies potentielles et suggérer des améliorations.
- Générer des conditions de test en utilisant la base de test , par exemple, pour les
  exigences/User Stories : les LLMs peuvent analyser les exigences et les User Stories afin de
  générer des conditions de test. Grâce au traitement du langage naturel , ils peuvent interpréter la
  signification des exigences et les décomposer en instructions mesurables et testables. Cela peut
  aider à traduire les exigences en conditions de test spécifiques.
- Hiérarchiser les conditions de test en fonction du niveau de risque : Grâce aux informations
  sur la probabilité du risque et l'impact du risque de défaillance pour chaque condition de test , un

LLM peut aider à hiérarchiser les efforts de test. En tenant compte d'aspects tels que la conformité
réglementaire, les fonctionnalités destinées aux utilisateurs (par exemple, la fonctionnalité de
connexion ou le traitement des paiements) et les données historiques sur les défauts, le LLM peut
recommander des niveaux de priorité.

- Aider à l'analyse de la couverture : En cartographiant les exigences et les User Stories aux
  conditions de test, un LLM peut effectuer une analyse de couverture afin de déterminer si tous les
  aspects de la base de test sont couverts. Ceci est particulièrement utile pour les projets aux
  exigences complexes, où des lacunes dans la couverture peuvent entraîner des défauts manqués.
- Suggérer des techniques de test : L'IA générative peut suggérer des techniques de test
  pertinentes (par exemple, analyse des valeurs limites, partition d'équivalence) en fonction du type
  d'exigence ou de User Story testée. Cela peut aider les testeurs à appliquer les techniques de test
  les plus efficaces pour des conditions de test spécifiques.
  La qualité et la pertinence des entrées fournies au LLM par rapport à la tâche à accomplir ont une incidence
  directe sur l'exactitude et la précision des résultats générés par le LLM.

Objectif d'apprentissage pratique 2.2.1a (H2): S'entraîner à créer des prompts multimodaux
structurés afin de générer des critères d'acceptation pour une User Story basée sur une maquette
d'interface graphique.
Il s'agit d'un exercice visant à s'entraîner à rédiger des prompts structurés à l'aide d'entrées multimodales
(texte et image). L'objectif est de générer des critères d'acceptation de haute qualité (c'est -à-dire bien
formés, clairs et complets) à partir d'une User Story et d'un wireframe d'interface graphique. D'autres
éléments textuels peuvent être ajoutés pour fournir du contexte, tels que des contraintes sur les champs
d'entrée ou des règles métier à appliquer au traitement des données.
Les résultats obtenus à partir du LLM sont comparés afin d'évaluer l'impact de différentes formulations
de la prompt structuré (rôle, contexte, instruction, données d'entrée textuelles et image, contraintes et
format de sortie) pour une tâche d'analyse de test.
Cet exercice permet d'acquérir une expérience pratique de l'importance d'une structuration des prompts,
de la contribution d'instructions précises et de l'importance des données contextuelles textuelles et
visuelles pour obtenir des résultats précis et pertinents à partir du LLM.

Objectif d'apprentissage pratique 2.2.1b (H2): Pratiquer l'enchaînement de prompts et la
vérification humaine pour analyser progressivement une User Story donnée et affiner les critères
d'acceptation.
Il s'agit d'un exercice visant à mettre en pratique l'enchaînement de prompts afin d'analyser une User
Story donnée et de peaufiner les critères d'acceptation , en identifiant d'abord les ambiguïtés, puis en
évaluant la testabilité et enfin en évaluant l'exhaustivité. Cet exercice encourage une approche étape
par étape, en affinant l'analyse à chaque étape afin de s'assurer que les critères d'acceptation sont bien
formulés et exploitables pour atteindre les objectifs du test. À chaque étape, les résultats fournis par le
LLM sont vérifiés manuellement et corrigés, si nécessaire, soit en ajustant la sortie, soit par un processus
d'enchaînement de prompts avec le LLM. De cette manière, l'étape suivante utilise un résultat propre de
l'étape précédente pour aborder un autre aspect de l'amélioration des critères d'acceptation.

Cet exercice permet de découvrir de manière pratique les avantages de décomposer une tâche
complexe en sous-tâches, avec vérification humaine des résultats de chaque étape.

### 2.2.2 Conception et implémentation des tests avec l'IA générative

Comme décrit dans [ISTQB_CTFL_SYL], la conception des tests implique l'élaboration et l'affinage des
conditions de test, qui sont ensuite traduites en cas de test et autre testware. L'implémentation des tests
implique la création ou l'acquisition du testware nécessaire pour exécuter les tests .
Les tests manuels et les scripts de test automatisés peuvent être créés, priorisés et organisés dans un
calendrier d'exécution des tests avec le support de l'IA générative . L'IA générative peut aider de manière
significative ce large groupe d'activités de test en facilitant la création et l'évaluation de divers testware,
notamment des cas de test, des données de test, des scripts de test et des environnements de test.
Voici quelques tâches typiques de conception et d'implémentation de tests qui peuvent être prises en
charge par l'IA générative:

- Génération de cas de test : Le traitement du langage naturel permet à l'IA générative de créer
  des versions préliminaires de cas de test basé es sur des exigences fonctionnelles et non
  fonctionnelles. Lorsqu'il est prompté avec des informations appropriées, un LLM peut suggérer des
  préconditions et des entrées de test, des résultats attendus et des critères de couverture ;
  produisant ainsi des cas de test qui répondent à différents objectifs de test, de la vérification
  fonctionnelle de base aux tests de bout en bout complexes.
- Synthèse des données de test : L'IA générative peut créer des données de test synthétiques
  représentatives et respectueuses de la confidentialité des données, qui ressemblent aux données
  de production et qui couvrent des situations extrêmes et des conditions de test variées. Ces
  données de test synthétiques peuvent être utilisées pour des tests fonctionnels et non fonctionnels.
  Les données de test générées par l'IA peuvent être adaptées aux exigences des appli cations,
  simulant des scénarios réalistes, sans exposer d'informations sensibles.
- Génération de scripts de test automatisés : L'IA générative peut générer des procédures de test
  manuelles et des scripts de test automatisés à partir de cas de test structurés, en interprétant les
  étapes de test et en les traduisant en code compatible avec divers frameworks d'automatisation
  des tests. Ces scripts de test peuvent être mis à jour ou étendus en fonction des nouvelles
  exigences.
- Planification et hiérarchisation de l'exécution des tests : L'IA générative peut analyser les cas
  de test et leurs interdépendances, optimisant ainsi les calendriers d'exécution des tests en fonction
  de la priorité, des risques associés, de la disponibilité des ressources et des objectifs des tests .

Objectif d'apprentissage pratique 2.2.2a (H2) : Pratiquer la génération de cas de test fonctionnel
à partir de User Stories avec l'IA en utilisant l'enchaînement de prompts, les prompts structurés
et les méta-prompts
Cet exercice se concentre sur le développement de cas de test fonctionnels à partir de User Stories avec
l'IA générative, en utilisant l'enchaînement de prompts, les prompts structurés et les techniques de méta-
prompting, pour garantir une couverture complète. La première étape consiste à créer un prompt qui
demande à l'IA de générer des cas de test fonctionnels basés sur des critères d'acceptation donnés et
suivant un format de sortie spécifique. La deuxième étape consiste à vérifier l'exhaustivité des cas de
test générés. Ici, le prompt vérifie que chaque critère d'acceptation est couvert en demandant à l'IA de
générer un tableau récapitulant la couverture. Enfin, la troisième étape consiste à créer un méta-prompt
pour faciliter la création de procédures de test de bout en bout. Ce méta -prompt permet d'affiner le
prompt afin de générer des tests de bout en bout complets, encourageant ainsi les améliorations
itératives pour maximiser l'efficacité.
Cet exercice améliore la compréhension de l'utilisation des LLMs pour la génération de cas de test , la
validation de la couverture et les tests de bout en bout.

Objectif d'apprentissage pratique 2.2.2b (H2) : Utiliser la technique few -shot prompting pour
générer des cas de test de style Gherkin à partir de User Stories données.
Cet exercice consiste à utiliser le few -shot prompting pour générer des cas de test de style Gherkin à
partir de User Stories données. En commençant par une revue d'exemples prédéfinis et de la syntaxe
Gherkin, l'étape 1 consiste à sélectionner n exemples à inclure dans le prompt, chacun avec une User
Story, des conditions de test et des cas de test attendus de type « étant donné – lorsque - alors » pour
modéliser le résultat souhaité. Ce prompt est ensuite appliqué à une nouvelle User Story, générant des
scénarios Gherkin qui reflètent les conditions de test d'origine. Si les résultats sont inexacts, le prompt
ou les exemples doivent être remaniés.
Cet exercice permet d'acquérir de l'expérience dans l'application des techniques de few -shot prompting
à des tâches réalistes de conception et d'implémentation de tests.

Objectif d'apprentissage pratique 2.2.2c (H2): Utiliser l'enchaînement de prompts pour
hiérarchiser les cas de test au sein d'une suite de tests donnée, en tenant compte de leurs
priorités et dépendances spécifiques
Cet exercice se concentre sur l'utilisation de l'IA générative pour améliorer la priorisation des cas de test
dans une suite de tests donnée, avec une analyse des risques associés et des dépendances entre les
cas de test. La session commence par un bref aperçu des différentes approches de test, telles que celles
basées sur les risques, sur la couverture et sur le s exigences, ainsi qu'une revue de la suite de tests
donnée. Les participants réalisent ensuite la création de prompts afin de générer des plans de
priorisation exploitables pour diverses stratégies de priorisation des tests. Les résultats du LLM basés
sur le prompt et les données d'entrée fournies doivent être vérifiés manuellement afin de détecter toute
erreur dans le raisonnement du LLM.
L'objectif de cet exercice est d'expérimenter l'IA générative sur des tâches de test qui nécessitent des
capacités de raisonnement multicritères (ici, les différents risques et dépendances à prendre en compte
pour la priorisation des cas de test).

### 2.2.3 Tests de régression automatisés avec l'IA générative

À mesure que chaque nouvelle itération ou release est terminée, le nombre de cas de test de régression à
exécuter augmente généralement, ce qui en fait des candidats idéaux pour l'automatisation, en particulier
dans les pipelines d'intégration continue / livraison continue (CI/CD) , en raison de la fréquence élevée

d'exécution des tests. L'IA générative peut rationaliser ce processus en facilitant la création, la maintenance
et l'optimisation des suites de tests de régression automatisés. En s'adaptant dynamiquement aux
modifications du code et en effectuant des analyses d'impact, l'IA générative peut id entifier les zones du
logiciel les plus susceptibles d'être affectées par les modifications récentes, ce qui permet de concentrer
les efforts de test de régression là où ils sont le plus nécessaires.
Voici quelques activités typiques de tests de régression automatisés et de reporting des tests qui peuvent
être prises en charge par le prompting avec l'IA générative :

- Implémentation de scripts de test automatisés basés sur des mots -clés : Les LLMs peuvent
  être utilisés pour implémenter des scripts de test basés sur des frameworks d'automatisation des
  tests basés sur des mots -clés, où des mots -clés prédéfinis représentent des étapes de test
  courantes. L'IA générative peut cartographier ces mots -clés vers des cas de test spécifiques,
  générer des scripts de test et assister les testeurs et les ingénieurs en automatisation des tests
  dans leur travail.
- Analyse d'impact et optimisation des tests : L'IA générative peut être utilisée pour analyser les
  modifications apportées au code afin d'identifier les zones à haut risque, permettant ainsi de cibler
  les tests de régression là où ils sont le plus nécessaires.
- Tests auto -réparateurs et adaptatifs : L'IA générative peut être utilisée pour ajuster
  automatiquement les scripts de test afin de gérer les modifications mineures de l'interface
  utilisateur ou de l'API, évitant ainsi les défaillances inutiles dues à de petites modifications et
  garantissant la stabilité des suites de tests au fil du temps.
- Reporting automatisé des tests et informations détaillées : L'IA générative permet de générer
  des rapports de test détaillés et disponibles en temps opportun, avec des métriques de réussite,
  les défaillances et les informations clés, fournissant ainsi aux parties prenantes des tableaux de
  bord qui mettent en évidence les tendance s des tests et offrent des informations prédictives sur
  les points de défaillance potentiels.
- Amélioration des rapports de défauts et de l'analyse des causes racines : L'IA générative peut
  prendre en charge la compilation automatique de rapports de défauts complets avec des logs de
  test, des captures d'écran et des données sur l'environnement de test.
  Ces activités peuvent être appliquées à divers tests de régression fonctionnels et non fonctionnels.
  Cependant, les testeurs doivent être conscients que l'IA générative peut faire des erreurs. La sortie générée
  doit donc être soigneusement vérifiée, en fonction du risque associé (voir chapitre 3) .
  En outre, l'IA générative peut faciliter les tests de régression automatisés de bout en bout basés sur
  l'interface graphique et l'API, chacun présentant ses propres défis et solutions. Les tests de l'interface
  graphique deviennent souvent instables en raison des changements récurr ents apportés à l'interface
  utilisateur. L'IA générative peut adapter automatiquement les scripts de test pour gérer des changements
  tels que les localisateurs dynamiques et les interactions modifiées, réduisant ainsi le besoin d'intervention
  manuelle. Les tests de régression des API sont confrontés à des défis tels que la modification des formats
  de requête/réponse, des points de terminaison et de l'authentification. L'IA générative peut adapter
  automatiquement les scripts de test aux spécifications API en constante évolution et générer diverses
  données de test, ce qui permet de maintenir une couverture complète et de réduire le besoin de mises à
  jour manuelles.

Objectif d'apprentissage pratique 2.2.3a (H2): Pratiquer le few-shot prompting pour créer et gérer
des scripts de test basés sur des mots-clés
Cet exercice se concentre sur le développement et l'automatisation de scripts de test pour une
application web donnée à l'aide d'un framework d'automatisation des tests de l'interface graphique.
L'exercice est structuré en deux sections principales : l'aut omatisation des tests et le débogage des
scripts de test. La première partie de l'exercice fournit des conseils sur la création d'une documentation
pour une bibliothèque de mots -clés, la génération de scripts de test initiaux, la validation de ces scripts
de test par l'IA et l'extension de la couverture avec des scripts de test supplémentaires. La deuxième
partie met l'accent sur le soutien au débogage, en utilisant des prompts système pour créer un assistant
IA capable de vérifier et de corriger les scripts de test.
Cet exercice combine l'automatisation traditionnelle des tests avec la validation assistée par l'IA,
démontrant comment le few -shot prompting peut être utilisé efficacement pour créer, maintenir et
déboguer des scripts de test basés sur des mots-clés.

Objectif d'apprentissage pratique 2.2.3b (H2): Pratiquer la rédaction de prompts structurés pour
l'analyse de rapports de test dans le contexte des tests de régression
Cet exercice illustre une approche méthodique de l'analyse des rapports de tests de régression, à l'aide
de prompts structurés. Le processus commence par une analyse des résultats des tests fournis et une
comparaison avec la spécification des tests. Il se poursuit ensuite par le regroupement des défauts
similaires, la maintenance d'une liste d'anomalies connues et une vérification croisée des constatations.
Chaque étape est liée à la suivante dans une conversation LLM s’enchaînant.
L'approche étape par étape montre comment des prompts structurés peuvent être utilisées pour
transformer les résultats des tests de régression et les logs de test en informations exploitables,
soutenant ainsi une analyse efficace des rapports de test dans le contexte des tests de régression .

### 2.2.4 Suivi des tests et contrôle des tests avec l'IA générative

Les tâches de suivi des tests nécessitent la récupération de grandes quantités de données (parfois non
structurées), qui sont souvent déjà disponibles dans des outils de gestion des tests que l'IA générative peut
aider à analyser et à synthétiser.
L'IA générative facilite un certain nombre de tâches de suivi et de contrôle des tests, notamment :

- Suivi des tests et analyse des métriques : L'IA générative peut faciliter l'automatisation du suivi
  des tests, ainsi que l'analyse des tendances afin de prévoir les risques potentiels et d'alerter les
  équipes en cas d'écart par rapport au plan. Les équipes restent ainsi informées et peuvent prendre
  les mesures nécessaires pour maintenir les normes de qualité.
- Contrôle des activités de test : L'IA générative peut faciliter le contrôle des tests en fournissant
  des informations permettant de redéfinir les priorités, d'ajuster le calendrier des tests et de
  réaffecter les ressources si nécessaire. Cela garantit que les tests restent flexibles et axés sur les
  domaines hautement prioritaires.
- Informations sur la clôture des tests et apprentissage continu : L'IA générative peut aider en
  générant des rapports de clôture de test, mettant en évidence les réussites et les leçons apprises.

Cela permet aux équipes d'affiner leurs stratégies de test et d'améliorer les processus de test
futurs.

- Visualisation et reporting améliorés des métriques de test : L'IA générative peut aider à créer
  des tableaux de bord dynamiques et des résumés en langage naturel, garantissant ainsi que toutes
  les parties prenantes ont accès aux métriques pertinentes. Cette aide fournit les informations
  nécessaires pour prendre des décisions rapid es et offre une vision claire de la progression des
  tests.

Objectif d'apprentissage pratique 2.2.4 (H0): Observer les métriques de suivi des tests préparées
par l'IA à partir des données de test
Cette démonstration illustre comment l'IA générative peut aider les équipes de test en transformant les
données de test en métriques de suivi des tests exploitables, facilitant ainsi la prise de décisions
éclairées. À partir des données de test extraites des outils de test, un LLM les traite pour générer des
métriques clés telles que la progression des tests, les tendances des défauts ou la couverture, mettant
en évidence les risques potentiels. Ces métriques générées par l'IA peuvent ensuite être affichées sur
un tableau de bord et résumées en langage naturel pour être facilement comprises par toutes les parties
prenantes.
Cette démonstration illustre comment l'IA générative transforme les données de test en informations
pratiques, aidant les équipes de test à suivre la progression des tests, à gérer la qualité et à s'adapter
rapidement aux changements.

### 2.2.5 Choisir des techniques de prompting pour les tests logiciels

Le tableau suivant montre l'adéquation des trois techniques de prompting mentionnées à la section 2.1.2 en fonction des caractéristiques de la tâche de test.
| **Technique de prompting** | **Cas d'utilisation recommandé** | **Principales caractéristiques et applications** |
|---|---|---|
| _Enchaînement de prompts_ | Tâches complexes nécessitant une vérification humaine à chaque étape | Divise les tâches en étapes plus petites, utiles pour l'analyse des tests, la conception des tests et l'automatisation des tests, où chaque étape du test est vérifiée pour s'assurer de son exactitude. |
| _Few-shot prompting_ | Tâches répétitives ou spécifiques / contraintes en matière de format de sortie | Fournit des exemples à l'IA générative pour la génération répétitive avec un canevas spécifique, par exemple dans un cas de test de style Gherkin (basé sur un scénario), des tests dirigés par les mots-clés ou le reporting des tests avec un format de sortie spécifique. |
| _Méta-prompting_ | Tâches flexibles et dynamiques, utiles pour créer des prompts pour de nouvelles tâches | Description générale de l'objectif et de la tâche à accomplir, qui guide le LLM dans la création du prompt. Utile pour toutes sortes de tâches complexes telles que l'analyse de rapports de test et la détection d'anomalies. |

Il est aussi possible d'utiliser plusieurs techniques pour un même cas d'utilisation. Par exemple, le méta -
prompting peut être utilisé pour créer un prompt initial. Ce prompt généré peut contenir des exemples qui
doivent être adaptés et peut être améliorés (few-shot prompting). Enfin, il peut être utile de diviser la tâche
en sous-tâches plus petites afin de permettre la validation des étapes intermédiaires (enchaînement de
prompts).

Objectif d'apprentissage pratique 2.2.5 (H1) : Sélectionner des techniques de prompting adaptées
au contexte pour des tâches de test données
Cet exercice se concentre sur la sélection de techniques de prompting appropriées pour différentes
tâches de test. Les participants se voient attribuer plusieurs tâches de test présentant différents niveaux
de difficulté. Pour chaque tâche de test, les participants doivent évaluer la nature de la tâche (nécessite-
t-elle de la précision ou une structure répétitive ?) et suggérer la ou les techniques de prompting les
mieux adaptées au contexte afin de répondre aux besoins spécifiques de la tâche. Les choix so nt
discutés en groupe.
Cet exercice est conçu pour approfondir la compréhension de la manière dont différentes techniques de
prompting peuvent être utilisées efficacement dans le cadre d’activités de test logiciel.

## 2.3 Évaluer les résultats de l'IA générative et affiner les prompts pour les tâches de test logiciel

L'évaluation des performances de l'IA générative dans le domaine des tests logiciels nécessite un
ensemble clair de métriques permettant d'évaluer la qualité, la pertinence et l'efficacité des résultats
générés (Li 2024). Ces métriques, qu'elles soient générales ou spécifiques à une tâche, contribuent à
optimiser les prompts LLM.

### 2.3.1 Métriques pour évaluer les résultats de l'IA générative sur des tâches de test

Plusieurs métriques peuvent être utilisées pour évaluer la qualité et l'efficience des résultats de l'IA
générative sur une tâche test :

| **Métrique**                            | **Description**                                                                                                                               | **Exemple**                                                                                                                                                                             |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| _Exactitude_                            | Mesure l'exactitude globale de la sortie générée par rapport à des cas de test rédigés par des experts, à des exigences ou à d'autres normes. | Le degré de couverture de toutes les exigences spécifiées par les cas de test générés.                                                                                                  |
| _Précision_                             | Évalue l'exactitude de la sortie générée par rapport à un objectif spécifique.                                                                | Le degré auquel les cas de test générés identifient correctement les anomalies.                                                                                                         |
| _Rappel_                                | Mesure la capacité d'un modèle à identifier toutes les instances pertinentes dans un ensemble de données.                                     | Le degré auquel les cas de test générés couvrent la partition d'équivalence valide et invalide d'une classe de données.                                                                 |
| _Pertinence et adéquation contextuelle_ | Détermine si le résultat généré est applicable et approprié dans un contexte donné.                                                           | Le degré de cohérence des cas de test générés avec la base de test et l'intégration des exigences spécifiques au domaine.                                                               |
| _Diversité_                             | Garantit la prise en charge d'un large éventail d'entrées et de scénarios, évitant ainsi les répétitions.                                     | Le degré auquel les cas de test générés couvrent divers comportements des utilisateurs et explorent les cas aux limites.                                                                |
| _Taux de réussite des exécutions_       | Mesure la proportion de cas de test ou de scripts de test générés qui peuvent être exécutés avec succès.                                      | Déterminer combien de scripts de test générés peuvent être exécutés sans erreurs de syntaxe ni problèmes de format de sortie dans un environnement de test qui fonctionne correctement. |
| _Efficience temporelle_                 | Évalue le temps gagné par rapport au test manuel.                                                                                             | Temps nécessaire à l'IA pour générer des cas de test par rapport au temps qu'il faudrait à un humain pour créer manuellement des tests équivalents.                                     |

En plus de ces métriques générales, des métriques spécifiques aux tâches peuvent être adaptées pour
évaluer dans quelle mesure l'IA générative prend en charge des activités de test spécifiques.
Pour évaluer efficacement ces métriques, les testeurs peuvent effectuer des revues manuelles ou les
automatiser, par exemple en comparant la sortie du LLM à une référence prédéfinie. Compte tenu de la
nature non déterministe de l'IA générative , les métriques doivent être basées sur des données
statistiquement pertinentes.

Objectif d'apprentissage pratique 2.3.1 (H0) : Observer comment les métriques peuvent être
utilisées pour évaluer le résultat de l'IA générative sur une tâche de test
Au cours d'une démonstration sur une tâche de test donnée, des métriques adaptées à la tâche sont
présentées pour évaluer les résultats de l'IA générative, ainsi que leur application concrète aux résultats
obtenus avec un LLM sur cette tâche de test.
Cette démonstration illustre l'importance des métriques d'évaluation pour garantir la fiabilité des résultats
de l'IA générative dans le domaine des tests logiciels.

### 2.3.2 Techniques d'évaluation et d'affinage itératif des prompts

Sur la base des métriques présentées ci-dessus, des techniques spécifiques d'évaluation et d'affinage sont
utilisées pour améliorer les résultats de l'IA :

- Modification itérative des prompts : Commencer par un prompt de base et le modifier de manière
  itérative en fonction des résultats observés, en ajoutant progressivement plus de contexte ou en
  ajustant la formulation (par exemple en ce qui concerne la terminologie) afin d'améliorer la
  spécificité et la pertinence.
- Tests A/B des prompts : Création de plusieurs versions de prompts et évaluation pour détecter
  celui qui produit les meilleurs résultats en fonction de métriques prédéfinies. Cette approche permet
  de déterminer la formulation ou la structure de prompt qui produit les résultats les plus précis et les
  plus pertinents.
- Analyse des résultats : Examen des résultats générés par l'IA afin de détecter les inexactitudes
  ou les incohérences, par exemple par rapport à la base de test. La compréhension des types
  d'erreurs et d'incohérences peut aider à affiner les prompts afin d'éviter des défauts similaires lors
  des itérations suivantes.
- Intégration des retours des utilisateurs : Recueillir les commentaires des testeurs sur l'utilité et
  la clarté des résultats générés, par exemple en ce qui concerne le niveau de détail des tests
  générés. Analyser leurs commentaires et les utiliser pour affiner les prompts afin de mieux
  répondre aux besoins réels en matière de test.
- Ajustement de la longueur et de la spécificité des prompts : Essais de différentes longueurs
  de prompts et différents niveaux de détail. Parfois, l’ajout de contexte supplémentaire peut
  améliorer la qualité de la réponse. Dans d'autres cas, des prompts plus courts peuvent donner lieu
  à de meilleurs résultats.
  En utilisant ces techniques, les équipes de test peuvent organiser des sessions d'évaluation et
  d'optimisation des prompts afin d'assurer l'amélioration continue d u prompting de l'IA générative . Le
  partage des pratiques au sein de l'équipe de test ou de l'organisation de test permet non seulement de
  normaliser les techniques de prompting et de maintenir une qualité constante, mais aussi de promouvoir
  une culture d'apprentissage et d'amélioration itérative. Cette approche collaborative contribue à l'évolution
  des méthodologies de test de l'IA générative en permettant aux équipes de test : de s'appuyer sur des
  connaissances collectives, d'éviter les erreurs répétées et d'affiner plus efficacement l eur utilisation des
  outils d'IA générative au fil du temps, par exemple en partageant des bibliothèques de prompts .

Objectif d'apprentissage pratique 2.3.2 (H1) : Évaluer et optimiser un prompt pour une tâche de
test donnée
Cet exercice se concentre sur l'application de techniques d'optimisation des prompts à une tâche de test
donnée. Les participants commenceront par un prompt initial et le remanieront de manière itérative afin
d'améliorer les résultats générés par l'IA. Ils utiliseront des techniques telles que les tests A/B et la
vérification humaine pour évaluer et améliorer la qualité des prompts. L'objectif est de permettre aux
participants de découvrir comment le remaniement itératif conduit à une génération de cas de test plus
efficace et plus pertinente dans le contexte.
À la fin de l'exercice, les participants auront effectué plusieurs itérations de remaniement des prompts et
évalué chaque itération à l'aide des métriques discutées afin d'améliorer la qualité des résultats de l'IA .
