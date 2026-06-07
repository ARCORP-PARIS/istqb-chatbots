# 4 Infrastructure de test basée sur LLM pour les tests logiciels

### Mots-clés

infrastructure de test

### Termes de l’IA générative

agent basé sur LLM, , base de données vectorielle, exploitation de grands modèles de langage
(LLMOps), fine-tuning, Retrieval-Augmented Generation (RAG)

### Objectifs d'apprentissage et objectifs d'apprentissage pratique pour le chapitre 4 :

## 4.1 Approches architecturales pour les infrastructures de test basées sur LLM

- **GenAI-4.1.1 (K2) Expliquer les principaux composants architecturaux et concepts de l'infrastructure de test basée sur LLM**
- **GenAI-4.1.2 (K2) Résumer les principes de la technologie Retrieval-Augmented Generation**
- **HO-4.1.2 (H1) Expérimentation de la technologie Retrieval-Augmented Generation sur une tâche de test donnée**
- **GenAI-4.1.3 (K2) Expliquer le rôle et l'application des agents basés sur LLM dans l'automatisation des processus de test**
- **HO-4.1.3 (H0) Observation d’ un agent basé sur LLM pour automatiser une tâche de test répétitive**

## 4.2 Fine-Tuning et LLMOps : opérationnalisation de l'IA générative pour les tests logiciels

- **GenAI-4.2.1 (K2) Expliquer le fine -tuning des modèles de langage pour des tâches de test spécifiques**
- **HO-4.2.1 (H0) Observer un exemple de processus de fine-tuning pour une tâche de test et un modèle de langage donnés**
- **GenAI-4.2.2 (K2) Expliquer les LLMOps et leur rôle dans le déploiement et la gestion des LLMs pour les tâches de test**

## 4.1 Approches architecturales pour les infrastructures de test basées sur LLM

Les chatbots IA et les outils de test basés sur les LLM s sont deux types d'infrastructures de test utilisant
les LLM (voir section 1.2.2).
Au-delà de l'architecture de base d'une infrastructure de test basée sur LLM (voir section 4.1.1), l e
Retrieval-Augmented Generation (voir section 4.1.2) et les architectures d'agents basés sur LLM (voir
section 4.1.3) étendent les fonctionnalités et l'utilité des LLM dans les tests logiciels.

### 4.1.1 Composants architecturaux clés et concepts de l'infrastructure de test basée LLM

Une infrastructure de test basée LLM fait référence à un système qui intègre un LLM dans le processus de
test logiciel afin d'améliorer l'automatisation, le raisonnement et la prise de décision. Contrairement à un
chatbot IA traditionnel, qui se concentre principalement sur les interactions conversationnelles, un outil de
test basé sur LLM est conçu pour prendre en charge les tests logiciels en traitant les prompts liés aux tests,
par exemple en analysant les exigences, en générant des cas de test et en évaluant les résultats.
L'architecture type d'une infrastructure de test basée sur LLM suit une conception à plusieurs composants
qui facilite une interaction sécurisée et efficace avec le LLM. L'architecture se compose de composants
front-end et back-end, ainsi que de sources de données externes et d'un LLM intégré :

- Le front-end sert d'interface utilisateur où les testeurs interagissent avec le système en saisissant
  des requêtes ou des commandes.
- Le back-end traite les entrées utilisateur et gère les fonctions critiques telles que l'authentification,
  la récupération des données, la préparation des prompts et l'interaction avec le LLM .
- Le LLM, qui peut être hébergé en tant que service tiers (accessible via une API) ou en tant que
  modèle interne personnalisé, génère des réponses basées sur des prompts structurés.
  Cette architecture va au -delà du modèle client -serveur traditionnel en intégrant des composants de
  traitement intelligents, tels que les LLMs et les back-ends multi-sources :

1. Le LLM n'est pas seulement un serveur, mais un composant de traitement intelligent qui interprète
   et raisonne en fonction des produits testés.
2. Contrairement aux chatbots basés sur des règles qui suivent des réponses scriptées, une
   infrastructure de test basée sur LLM génère des informations de test de manière dynamique à
   partir du contexte, tel que les exigences, le code ou les résultats des tests.
3. Le back-end intègre plusieurs sources de données, telles que :
   o Des bases de données relationnelles (pour les données structurées utilisées dans les
   tests, telles que les cas de test).
   o Des bases de données vectorielles (pour la recherche sémantique de contenus connexes
   à l'aide d'embeddings ; voir section 4.1.2).

4. Le back-end améliore les résultats bruts du LLM grâce à un post-traitement, garantissant ainsi que
   ses réponses correspondent aux conditions de test du processus de test avant de les présenter au
   front-end.

### 4.1.2 Retrieval-Augmented Generation

La technologie Retrieval-Augmented Generation (RAG) améliore les LLMs en intégrant des sources de
données supplémentaires dans leur processus de génération de réponses (Zhao 2024), augmentant ainsi
la pertinence et la précision de leurs résultats.
Le RAG combine des systèmes de recherche avec des modèles de langage pour générer des réponses
adaptées au contexte. Lors du prétraitement, les documents volumineux sont divisés en petits morceaux
(par exemple, de 256 à 512 tokens) afin de garantir une recherche ciblée et la compatibilité avec la fenêtre
contextuelle du modèle. Chaque fragment est nettoyé, traité et encodé dans un vecteur de haute dimension
(embedding) à l'aide de modèles pré-entraînés. Ces embeddings, qui peuvent être stockés dans des bases
de données vectorielles, permettent une recherche efficace basée sur la similarité au moment de
l'exécution (inférence). Un prompt utilisateur est encodé, les fragments pertinents sont récupérés sur la
base de leur similarité sémantique, puis utilisés comme contexte pour le modèle de langage afin de générer
une réponse fondée.
Une réponse pertinente est essentiellement une sortie générée par le modèle de langage qui est
profondément enracinée dans des informations pertinentes, précises et adaptées au contexte, recueillies
pendant le processus de recherche. Elle garantit que la r éponse n'est pas seulement basée sur
l'entraînement préexistant du modèle, mais également enrichie par des données précises pertinentes pour
le prompt. Cette synergie entre la recherche et la génération améliore la précision et la pertinence des
réponses, les rendant plus fiables et plus informatives pour l'utilisateur.
Dans la phase de traitement des prompts utilisateur, un système RAG fonctionne selon un processus en
deux étapes :

1. Récupération : à partir d'un prompt utilisateur, le système récupère les informations pertinentes
   dans les bases de données vectorielles créées précédemment. Cette récupération repose
   généralement sur la similarité sémantique entre les embeddings du prompt et ceux des morceaux.
2. Génération : les informations récupérées sont ensuite transmises au LLM, qui génère une réponse
   combinant ses connaissances existantes et les données nouvellement acquises, ce qui permet
   d'obtenir un résultat plus précis et plus adapté au contexte.
   Le RAG dans les tests logiciels permet à l'infrastructure de test basée sur LLM d'accéder aux sources de
   données de l'entreprise, telles que les bases de données, la documentation et les référentiels, afin de
   récupérer des informations contextuelles en temps réel, garantissant ainsi que les tâches de test, telles
   que l'analyse ou la conception des tests, sont alignées sur les dernières spécifications, exigences et
   données de test existantes.

Objectif d'apprentissage pratique 4.1.2 (H1) : Expérimenter la technologie Retrieval -Augmented
Generation pour une tâche de test donnée
Cet exercice pratique se concentre sur l'application des techniques RAG à une tâche de test donnée.
Les participants expérimenteront un système RAG en y intégrant des documents et observeront
comment il génère des réponses plus ou moins précises à partir d'informations complexes. Les

participants compareront les résultats du LLM avec et sans RAG pour la tâche de test donnée. Cet
exercice vise à identifier les forces et les limites du système RAG dans le traitement de différents types
de tâches de test.
En examinant les données récupérées et les résultats générés, les participants comprendront mieux le
rôle du RAG dans l'amélioration des processus de test basés sur LLM.

### 4.1.3 Le rôle des agents basés sur LLM dans l'automatisation des processus de test

Les agents basés LLM (Wang 2024) sont des applications d'IA générative spécialisées, alimentées par des
LLMs et conçues pour le traitement semi-autonome ou autonome de tâches définies. À la base, ces agents
s'appuient sur les LLMs pour la compréhension et la génération du langage naturel, complétées par la
possibilité de traiter des instructions, de récupérer du contexte et de mener des actions intelligentes .
Contrairement aux chatbots IA traditionnels qui se concentrent uniquement sur les interactions question -
réponse, les agents basés sur LLM peuvent effectuer des tâches ou « agir » en invoquant un ensemble
prédéfini de fonctions, communément appelées « outils ». Cette capacité leur permet d'interagir avec des
systèmes externes et de les manipuler, ce qui les rend très polyvalents dans l'exécu tion des tâches. Le
degré d'autonomie des agents basés sur LLM peut varier :

- Les agents autonomes fonctionnent indépendamment, exécutant des tâches avec une intervention
  humaine minimale à l'aide de règles prédéfinies, d'un apprentissage par renforcement et de
  boucles de rétroaction adaptatives.
- Les agents semi-autonomes exécutent des tâches sous la supervision périodique d'un humain afin
  de garantir que le résultat correspond aux objectifs définis par l'utilisateur.
  Les architectures multi -agents impliquent un système collaboratif dans lequel plusieurs agents, chacun
  ayant des rôles spécialisés, communiquent et se coordonnent pour résoudre des problèmes complexes
  plus efficacement qu'un seul agent. Cet effort coordonn é entre plusieurs agents IA est appelé
  « orchestration ».
  Dans les processus de test, les agents basés sur LLM peuvent automatiser les tâches de test en émulant
  le raisonnement et la prise de décision humains. Cependant, ces agents souffrent des mêmes problèmes
  d'hallucinations, d'erreurs de raisonnement et de biais observés lors de l'utilisation des LLMs (voir section
  3.1). Ces agents peuvent produire des résultats incorrects ou trompeurs, ce qui peut affaiblir la fiabilité des
  processus de test automatisés. Ces risques peuvent être atténués en mettant en œuvre des procédures
  de vérification automatisées pour les résultats des agents ou en utilisant des agents semi-autonomes pour
  les tâches critiques.

Objectif d'apprentissage pratique 4.1.3 (H0) : Observer comment un agent basé LLM aide à
automatiser une tâche de test répétitive
La démonstration se concentre sur une tâche de test effectuée par un agent basé sur LLM. Les données
d'entrée passées à l'agent, son comportement et les résultats de ses actions seront présentés , afin
d'illustrer les différents aspects de l'intégration de solutions basées sur des agents dans un processus
de test.

Cette démonstration montre un exemple concret d'un agent basé LLM dans le contexte d'une tâche test.

## 4.2 Fine-tuning et LLMOps : opérationnalisation de l'IA générative pour les tests logiciels

Deux pratiques clés pour mettre en place et gérer une infrastructure de test basée sur LLM pour les tests
comprennent le fine-tuning des LLMs et la gestion du pipeline opérationnel via LLMOps (Mailach 2024).

### 4.2.1 Fine-tuning des LLMs pour les tâches de test

Le fine-tuning adapte un modèle de langage pré -entraîné, tel qu'un LLM ou un petit modèle de langage
(SLM, voir section 1.1.2), afin qu'il puisse effectuer des tâches spécifiques ou pour l’ajuster à des domaines
particuliers (Parthasarathy 2024). Cela implique de poursuivre l'entraînement du modèle sur un ensemble
de données ciblé, lui permettant ainsi d'acquérir des connaissances et des nuances spécifiques au
domaine. Le fine -tuning améliore les pe rformances du modèle pour des applications spécialisées, le
rendant plus précis et plus pertinent pour le cas d'utilisation prévu.
Dans la pratique, le fine-tuning est approprié pour doter les LLMs génériques de capacités de raisonnement
spécialisées pertinentes pour un domaine spécifique ou pour adopter un vocabulaire propre à ce domaine.
Le fine -tuning peut également être appliqué à des modèles plus petits, appelés SLM s, qui sont moins
gourmands en ressources. En affinant un SLM (fine-tuning), il est possible d'atteindre des niveaux de
performance plus élevés pour des tâches spécifiques sans requérir la même charge informatique pour les
LLMs. Cette comparaison met en évidence la flexibilité et l'efficience de l'utilisation des LLMs et des SLMs
en fonction des exigences spécifiques de la tâche.
Par exemple, dans le domaine des tests logiciels, le fine -tuning peut permettre à un LLM ou à un SLM de
générer des cas de test à partir de User Stories dans un format de sortie spécifique au contexte de
l'organisation. En entraînant le modèle sur les User Stories de l'organisation et les cas de test
correspondants, le modèle s'aligne sur le processus de test et la terminologie spécifiques à l'organisation.
Le fine-tuning d'un modèle d'IA générative pour les tests logiciels présente plusieurs défis :

- Éviter les résultats biaisés ou inexacts tout en veillant à utiliser des ensembles de données
  d'entraînement de haute qualité et spécifiques à la tâche.
- Atténuer le surajustement (le modèle devient trop spécialisé dans les données d'entraînement, ce
  qui nuit à ses performances sur des données nouvelles et inconnues) afin de maintenir la
  généralisation dans différents scénarios.
- Remédier à l'opacité (manque de transparence dans la manière dont un LLM prend ses décisions
  ou produit ses résultats) dans le raisonnement du modèle, c ar l’opacité complique le débogage et
  la validation.
- Gérer les ressources informatiques significatives requises pour le processus de fine -tuning (pour
  les LLMs).

Objectif d'apprentissage pratique 4.2.1 (H0) : Observer un exemple de processus de fine -tuning
pour une tâche de test et un LLMSLM donnés
Cette démonstration montre les différentes étapes nécessaires au fine -tuning d'un LLM pour une tâche
de test donnée. Elle commence par la sélection d'un LLM ou SLM approprié. Ensuite, un ensemble de
données adapté à la tâche de test donnée est présenté. Puis, une solution type pour le processus de
fine-tuning est présentée (par exemple, un framework de machine learning). Enfin, un prompt est envoyé
au modèle affiné et la qualité de la sortie générée est discutée.
Cette démonstration du processus de fine -tuning LLM /SLM pour une tâche de test montre plusieurs
aspects clés de ce processus et aborde en particulier la qualité des données d'entraînement .

### 4.2.2 LLMOps lors du déploiement et de la gestion des LLMs pour les tests logiciels

LLMOps, ou Large Language Model Operations, désigne l'ensemble des pratiques, outils et processus
conçus pour rationaliser le développement, le déploiement et la maintenance des LLMs dans les
environnements de production (Sinha 2024).
L'utilisation de l'IA générative dans les processus de test d'une organisation peut se faire de différentes
manières, qui influenceront les décisions à prendre en matière de LLMOps. Voici trois approches possibles
:

- Utilisation d'un chatbot IA : les principales considérations pour cette approche comprennent la
  gestion de la confidentialité des données et des risques de sécurité tout en optimisant les coûts.
  Les organisations peuvent utiliser des plateformes LLM-as-a-Service, si les garanties nécessaires
  sont fournies, ou déployer une infrastructure interne utilisant des LLMs sous licence open source
  pour un meilleur contrôle. Un audit rigoureux des garanties des fournisseurs ou des capacités
  internes est essentiel pour atténuer les risques liés à la confidentialité et à la sécurité des données
  (voir section 3.2) et pour garantir l'efficience opérationnelle.
- Utilisation d'un outil de test doté de capacités d'IA générative : cette approche soulève des
  considérations similaires à celles des chatbots IA, telles que la confidentialité des données , la
  sécurité et les coûts opérationnels. En outre, les organisations doivent évaluer la sécurité des
  données et les garanties de performance offertes par le fournisseur de l'outil de test. Ces outils de
  test complètent généralement les processus de test existants, qui nécessitent une analyse coûts-
  avantages et une évaluation des risques approfondies.
- Développement en interne d'un outil de test basé sur l'IA générative : cette approche met
  l'accent sur le contrôle global de la confidentialité des données et des risques de sécurité , ainsi
  que sur la planification minutieuse des coûts d'exploitation de l'IA, tels que les ressources
  informatiques, le stockage des données et la formation du personnel. Les organisations doivent
  également mettre en place des processus structurés pour valider et maintenir les développements
  spécifiques à l'IA générative. Le développement de solutions en interne nécessite une expertise
  dans l'implémentation et le déploiement d'une infrastructure de test basée sur LLM.
  Ces approches ne s'excluent pas mutuellement, car une organisation peut utiliser un chatbot IA pour
  certaines tâches tout en développant des outils personnalisés pour d'autres. Elles peuvent donc être
  mises en œuvre simultanément en fonction des activités de test spécifiques concernées.

En outre, elles peuvent intégrer des technologies supplémentaires, telles que le RAG et le fine-tuning
des LLMs/SLMs, afin d'améliorer l'efficacité et l'adaptabilité des processus de test avec l'IA générative.
