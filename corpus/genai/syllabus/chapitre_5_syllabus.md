# 5 Déploiement et intégration de l'IA générative dans les organisations de test

### Mots-clés

Aucun

### Termes de l’IA générative

IA fantôme

### Objectifs d'apprentissage et objectifs d'apprentissage pratique pour le chapitre 5 :

## 5.1 Feuille de route pour l'adoption de l'IA générative dans les tests logiciels

- **GenAI-5.1.1 (K1) Rappeler les risques liés à l'IA fantôme**
- **GenAI-5.1.2 (K2) Expliquer les aspects clés à prendre en compte lors de la définition d'une stratégie d'IA générative pour les tests logiciels**
- **GenAI-5.1.3 (K2) Résumer les critères clés pour sélectionner les LLMs/SLMs pour les tâches de test logiciel dans un contexte donné**
- **HO-5.1.3 (H1) Estimer les coûts récurrents liés à l'utilisation de l'IA générative pour une tâche de test donnée**
- **GenAI-5.1.4 (K1) Rappeler les phases clés de l'adoption de l'IA générative dans une organisation test**

## 5.2 Gérer le changement lors de l'adoption de l'IA générative pour les tests logiciels

- **GenAI-5.2.1 (K2) Expliquer les compétences et les connaissances essentielles requises pour que les testeurs puissent travailler efficacement avec l'IA générative dans les processus de test**
- **GenAI-5.2.2 (K1) Rappeler les stratégies visant à développer les compétences en IA au sein des équipes de test afin de soutenir l'adoption de l'IA générative dans les activités de test**
- **GenAI-5.2.3 (K1) Reconnaître comment les processus de test et les responsabilités évoluent au sein d'une organisation de test lors de l'adoption de l'IA générative**

## 5.1 Feuille de route pour l'adoption de l'IA générative dans les tests logiciels

Une stratégie de test avec l'IA générative doit prendre soigneusement en compte des aspects clés tels que
les objectifs de test à atteindre, la sélection appropriée du LLM , les problèmes liés aux données d'entrée
utilisées pour les prompts et la conformité aux normes et réglementations en matière d'IA. Sur la base de
cette stratégie, l'organisation peut établir une feuille de route et suivre les progrès de l'intégration de l'IA
générative dans les processus de test.

### 5.1.1 Risques liés à l'IA fantôme

L'IA fantôme peut entraîner des risques en matière de sécurité , de conformité et de confidentialité des
données:

- Faiblesses en matière de sécurité de l'information et de confidentialité des données : les outils d'IA
  personnels peuvent présenter des lacunes en matière de sécurité, ce qui peut entraîner des
  violations de données.
- Conformité et questions réglementaires : L'utilisation d'outils d'IA non approuvés peut entraîner la
  non-conformité aux normes et réglementations de l'industrie (voir section 3.4.1), ce qui peut avoir
  des conséquences juridiques.
- Propriété intellectuelle vague : l'utilisation d'outils d'IA assortis d'accords de licence peu clairs peut
  exposer les utilisateurs de LLM à des litiges en matière de propriété intellectuelle, en particulier si
  des données protégées par le droit d'auteur sont traitées sans autorisation appropriée .
  Une stratégie et des étapes pour l'intégration et le déploiement de l'IA générative peuvent aider les
  organisations à tester et à éviter les risques liés à l'IA fantôme.

### 5.1.2 Aspects clés d'une stratégie d'IA générative dans le domaine des tests logiciels

Pour implémenter avec succès une stratégie d'IA générative dans les tests, les organisations doivent
examiner attentivement plusieurs facteurs clés afin de garantir une intégration fluide et des résultats
optimaux.
Cela commence par la définition d'objectifs de test mesurables pour l'IA générative, tels que l'augmentation
de la productivité des tests, le raccourcissement des cycles de test et l'amélioration de la qualité des tests.
Le choix des LLMs appropriés est essentiel (voir section 5.1.3) et doit être aligné sur ces objectifs de test,
tout en garantissant l a compatibilité avec l'infrastructure de test existante et en répondant aux exigences
de mise à l'échelle du système.
La qualité des données joue un rôle essentiel, car l'efficacité des tests basés sur LLM dépend de données
d'entrée précises et pertinentes, protégées par des procédures de sécurité robustes. Il est donc essentiel
de maintenir une qualité élevée des données d'entrée afin d'obtenir des résultats fiables .
Des programmes de formation complets devraient être proposés afin de garantir que les équipes de test
disposent des compétences techniques et éthiques nécessaires pour utiliser efficacement les outils d'IA
générative. Outre la formation, des métriques spécifiques devraient être collectées afin de mesurer
l'efficacité des résultats de l'IA générative (voir section 2.3.1).

Pour garantir la conformité aux normes réglementaires et le respect des directives éthiques, les
organisations doivent établir des directives pour l'utilisation de l'IA générative, y compris des règles relatives
à l'utilisation des données sensibles, des obligations de transparence (par exemple, ce qui a été généré à
l'aide de l'IA générative) et des contrôles de qualité avec revue des testware générés .

### 5.1.3 Sélectionner des LLMs/SLMs pour des tâches de test logiciel

Il existe une large gamme de LLMs/SLMs, chacun avec des capacités fonctionnelles différentes (par
exemple, entrée multimodale, capacités de raisonnement), des caractéristiques techniques (par exemple,
taille de la fenêtre contextuelle) et des types de licence (par exemple, commerciale ou open source). Bien
qu'il existe de nombreux benchmarks pour évaluer les LLMs/SLMs pour des tâches telles que le traitement
du langage naturel, la génération de code ou l'analyse d'images ; seuls quelques-uns sont spécifiquement
axés sur les tâches de test logiciel (Wenhan 2024). Par conséquent, la sélection des LLMs/SLMs pour les
tâches de test nécessite un examen attentif de plusieurs critères clés :

- Performances du modèle : évaluer les performances du modèle pour les tâches de test ciblées
  par rapport aux benchmarks de l'organisation , à l'aide de métriques telles que celles présentées
  dans la section 2.3.1.
- Potentiel de fine-tuning : évaluer s'il est possible et utile d'affiner le modèle de langage (LLM ou
  SLM) à l'aide de données spécifiques au domaine afin d'améliorer les performances pour un cas
  d'utilisation donné, en augmentant la précision et la pertinence dans des contextes spécialisés .
- Coût récurrent : tenir compte des coûts récurrents liés à l'utilisation du LLM /SLM, y compris les
  coûts de licence et les dépenses opérationnelles, afin de s'assurer qu'ils correspondent au budget
  de l'organisation pour les tâches de test ciblées.
- Communauté et assistance : choisir des modèles bénéficiant d'une communauté active et d'une
  documentation détaillée pour faciliter l'implémentation et le dépannage.
  En évaluant soigneusement ces critères, les organismes de test peuvent sélectionner un ou plusieurs
  LLMs/SLMs qui répondent à leurs besoins spécifiques et à leurs contraintes organisationnelles .

Objectif d'apprentissage pratique 5.1.3 (H1) : Estimation des coûts récurrents liés à l'utilisation
de l'IA générative pour une tâche de test donnée
Cet exercice se concentre sur l'estimation des coûts récurrents liés à l'utilisation de l'IA générative pour
une tâche de test spécifique, sur la base de diverses hypothèses. Ces hypothèses incluent des facteurs
tels que le nombre de tokens dans les données d'entrée et de sortie, les prompts utilisés et la fréquence
de la tâche. Les modèles de tarification de plusieurs fournisseurs de LLM /SLM seront explorés et
comparés, y compris au moins une solution commerciale et un modèle sous licence open source .
Cet exercice permet de calculer et d'expérimenter les coûts récurrents de l'IA générative à l'aide
d'hypothèses concrètes, ce qui aide à comprendre les implications financières des différentes approches
et des différents fournisseurs.

### 5.1.4 Phases d'adoption de l'IA générative dans les tests logiciels

L'adoption de l'IA générative au sein d'une organisation de test implique trois phases clés :

1. Découverte : La première phase se concentre sur la sensibilisation et le renforcement des
   capacités. Les activités comprennent la formation des équipes de test aux concepts de l'IA
   générative, l'accès aux LLMs/SLMs et l'expérimentation de cas d'utilisation initiaux afin de
   familiariser les testeurs avec l'IA générative et de renforcer leur confiance.
2. Initiation et définition de l'utilisation : une fois les bases acquises, la deuxième phase consiste
   à identifier et à hiérarchiser les cas d'utilisation pratiques de l'IA générative dans les tests logiciels.
   Cette phase comprend l'évaluation d'une infrastructure de test basée sur LLM, le développement
   d'une expertise et la mise en adéquation avec les besoins de l'organisation (voir
   [ISTQB_CTFL_SYL] section 6).
3. Utilisation et itération : à ce stade avancé, les organisations intègrent pleinement l'IA générative
   dans leurs processus de test. Un suivi continu de la progression de l'IA générative pour les tests
   logiciels et les outils associés est mis en place, ainsi que la mesure et la gestion de la
   transformation afin de garantir des avantages durables et l'évolutivité et le passage à l'échelle.
   Ces phases peuvent se dérouler en parallèle pour différents cas d'utilisation. Par exemple, l'analyse des
   rapports de test peut être plus avancée dans la feuille de route alors que l'automatisation des tests en est
   encore à ses débuts.
   Il est également important de reconnaître et de traiter rapidement les préoccupations telles que la crainte
   de perdre son emploi, qui peuvent avoir un impact sur l'adoption et le moral de l'équipe .

## 5.2 Gérer le changement lors de l'adoption de l'IA générative pour les tests logiciels

La mise en œuvre réussie de l'IA générative dans une organisation de test nécessite une approche
structurée des processus de gestion du changement. Les aspects clés comprennent le développement des
compétences essentielles en IA générative et l'évolution des rôles traditionnels du test afin d'intég rer les
processus de test basés sur l'IA. La transformation implique à la fois des compétences techniques et des
aspects organisationnels.

### 5.2.1 Compétences et connaissances essentielles pour tester avec l'IA générative

L'intégration réussie de l'IA générative dans les tests nécessite la maîtrise des techniques d'ingénierie du
prompting, la compréhension des fenêtres contextuelles des modèles et le développement de méthodes
de revue des tests. Les testeurs doivent combiner leur expertise du domaine et des tests avec des
compétences en IA, pour évaluer les tests basés sur le LLM dans des tâches telles que la génération de
cas de test, l'analyse des rapports de défauts et la génération de données de test .
Les compétences clés comprennent l'évaluation des capacités des LLM s, la compréhension des
techniques d'amélioration des prompts et l'évaluation des testware générés par l'IA.
Les connaissances essentielles incluent la compréhension des risques inhérents à l'IA générative , ainsi
que la connaissance des stratégies d'atténuation courantes. Les testeurs doivent comprendre les
implications, en matière de sécurité des données, du partage de logiciels de test avec les LLMs ; mettre en

œuvre une expurgation appropriée des données (suppression ou masquage des informations sensibles,
personnelles ou confidentielles) et suivre les pratiques d'ingénierie du prompting préservant la
confidentialité des données.
Les considérations environnementales comprennent l'optimisation de la sélection des modèles et des
canevas d'utilisation afin de réduire la charge informatique ; la sélection de modèles adaptés aux tâches
de test et l'équilibre entre les avantages de l'automatisation de l'IA générative et son impact sur les coûts
et la consommation d'énergie.

### 5.2.2 Développer des capacités d'IA générative au sein des équipes de test

Une approche pratique est essentielle pour former stratégiquement les équipes de test à l'IA générative .
Cela comprend la pratique avec divers LLMs/SLMs, le suivi de chemins d'apprentissage structurés et le
développement progressif d'un savoir -faire grâce au partage au sein de l'organisation. La formation est
axée sur le développement de compétences pratiques grâce à des exercices guidés, l'apprentissage entre
pairs et l'intégration progressive de l'IA dans les tâches de test quotidiennes.
Les membres de l'équipe de test passent de la maîtrise de la création de prompts de base à l'utilisation de
techniques plus ciblées, telles que les prompts spécifiques aux tests. Un canevas de prompt est un
template / gabarit réutilisable pour créer des prompts efficaces , afin de guider l'IA générative vers des
résultats cohérents et fiables.
Des communautés de pratique internes soutiennent le partage continu des connaissances, avec des
réunions régulières pour mettre en avant les applications réussies de l'IA générative, discuter des défis et
affiner les meilleures pratiques. Ces communautés f avorisent l'amélioration continue en partageant des
bibliothèques de canevas de prompts et en documentant les leçons tirées de l'IA générative pour
l'implémentation de tests dans différents projets et domaines.

### 5.2.3 Évolution des processus de test dans les organisations de test basées sur l'IA

L'intégration de l'IA générative transforme les processus de test traditionnels des testeurs et des
responsables de tests, au sein des organisations de test.
Les testeurs évoluent de spécialistes de la conception et de l'exécution des tests , à des spécialistes des
tests assistés par l'IA ; combinant leur expertise en techniques de test avec des compétences pour guider
et vérifier les testware générés par l'IA. Leurs tâches de test s'étendent à la revue de l'ensemble des
résultats basés sur l'IA, au remaniement des prompts et à la maintenance des bibliothèques de prompts
spécifiques aux tests.
Les responsabilités des responsables des tests évoluent afin d'inclure le développement d'une stratégie de
test basée sur l'IA, la gestion des risques basée sur l'IA, ainsi que le suivi et le contrôle des processus de
test basés sur l'IA. Les responsables des tests s'attachent à équilibrer les capacités humaines et celles de
l'IA, à établir des cadres de gouvernance de l'IA pour les cas d'utilisation et à veiller à ce que leurs équipes
de test conservent à la fois leurs compétences traditionnelles en matière de test et leurs connaissances en
matière d'IA. Les test managers ne se contenteront pas de diriger les testeurs humains, mais devront
également coordonner les agents de test basés sur l'IA générative , ce qui nécessitera de nouvelles
compétences en matière de management pour superviser des équipes hybrides composées d'humains et
d'outils d'IA générative.
