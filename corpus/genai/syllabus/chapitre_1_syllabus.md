# 1 Introduction à l'IA générative pour les tests logiciels –

### Mots-clés

None

### Termes de l’IA générative

chatbot IA, deep learning, embedding, feature, fenêtre contextuelle, grand modèle de langage (LLM), IA
générative, IA symbolique, LLM adapté aux instructions, LLM de fondation, LLM de raisonnement, machine
learning, modèle multimodal, tokenisation, Transformer, Transformer génératif pré-entraîné

### Objectifs d'apprentissage et objectifs d'apprentissage pratique pour le chapitre 1 :

## 1.1 Fondements et concepts clés de l'IA générative

- **GenAI-1.1.1 (K1) Rappeler différents types d'IA : IA symbolique, machine learning classique, deep learning et IA générative**
- **GenAI-1.1.2 (K2) Expliquer les bases de l'IA générative et des grands modèles de langage**
- **HO-1.1.2 (H1) Pratiquer la tokenisation et l'évaluation du nombre de tokens lorsque vous utilisez un LLM pour une tâche de test logiciel**
- **GenAI-1.1.3 (K2) Faire la différence entre LLM de base, LLM adapté aux instructions et LLM de raisonnement**
- **GenAI-1.1.4 (K2) Résumer les principes de base des modèles multimodaux de langage et des modèles de vision**
- **HO-1.1.4 (H1) Écrire et exécuter un prompt pour un LLM multimodal utilisant à la fois des entrées textuelles et des images pour une tâche de test logiciel**

## 1.2 Tirer parti de l'IA générative dans les tests logiciels : principes généraux

- **GenAI-1.2.1 (K2) Donner des exemples de capacités clés des LLMs pour les tâches de test**
- **GenAI-1.2.2 (K2) Comparer les modalités d'interaction lorsque vous utilisez l'IA générative pour tester des logiciels**

## 1.1 Fondements et concepts clés de l'IA générative

L'intelligence artificielle générative (IA générative) est une branche de l'intelligence artificielle qui utilise de
grands modèles pré-entraînés pour générer des résultats semblables à ceux d'un être humain, tels que du
texte, des images ou du code. Les grands modèles de langage (LLM ) sont des modèles d'IA générative
pré-entraînés sur de grands ensembles de données textuelles, ce qui leur permet de déterminer le contexte
et de produire des réponses pertinentes en fonction des requêtes des utilisateurs.
Les concepts clés comprennent la tokenisation (c'est-à-dire la division du texte en unités pour un traitement
efficace), les fenêtres contextuelles (limitation de la quantité d'informations prises en compte à la fois pour
maintenir la pertinence) et les modèles multimodaux (capables de traiter plusieurs types de données telles
que du texte, des images et de l'audio pour des interactions riches).
Dans le domaine des tests logiciels, ces LLM peuvent prendre en charge des tâches telles que la revue et
l'amélioration des critères d'acceptation , la génération de cas de test ou de scripts de test, l'identification
des défauts potentiels, l'analyse des canevas de défauts, la génération de données de test synthétiques
ou la prise en charge de la génération de documentation, et ce tout au long du processus de test.

### 1.1.1 Panorama de l'IA : IA symbolique, machine learning classique, deep learning et IA générative

L'intelligence artificielle (IA) est un vaste domaine qui englobe différents types de technologies, chacune
avec sa propre façon de résoudre les problèmes, telles que l'IA symbolique, le machine learning classique,
le deep learning et l'IA générative (entre autres technologies qui ne relèvent pas du périmètre de ce
syllabus) :

- L'IA symbolique utilise un système basé sur des règles pour imiter la prise de décision humaine.
  Essentiellement, l'IA symbolique représente les connaissances à l'aide de symboles et de règles
  logiques.
- Le machine learning classique est une approche basée sur les données qui nécessite la
  préparation des données, la sélection des caractéristiques et l'entraînement des modèles. Elle peut
  être utilisée pour des tâches telles que la catégorisation des défauts et la prédiction des problèmes
  logiciels.
- Le deep learning utilise des structures de machine learning , appelées réseaux neuronaux , pour
  apprendre automatiquement des features à partir de données. Les modèles de deep learning
  peuvent trouver des motifs dans des ensembles de données très volumineux et complexes, tels
  que des images, des vidéos, des fichiers audio ou du texte, sans que les utilisateurs aient besoin
  de définir manuellement des features. Dans la pratique, cela peut toutefois nécessiter une
  intervention humaine pour des tâches telles que l'annotation des données, le réglage des modèles
  ou la validation des résultats.
- L'IA générative utilise des techniques de deep learning pour créer de nouveaux contenus (textes,
  images, code) en apprenant et en imitant les canevas de ses données d'entraînement. Des
  modèles tels que les LLM peuvent générer du texte, écrire du code et simuler un raisonnement ou
  une résolution de problèmes dans le périmètre de leur entraînement.
  En résumé, le domaine de l'IA a évolué dans plusieurs directions, chacune présentant des avantages et
  des limites différents. Le principal avantage de l'utilisation de l'IA générative pour les tests logiciels réside
  dans le fait qu'elle utilise des modèles pré-entraînés qui peuvent être appliqués directement aux tâches de

test sans nécessiter de phase d'entraînement supplémentaire, bien que cela comporte certains risques
(voir section 3.1).

### 1.1.2 Notions de base sur l'IA générative et les LLMs

Basés sur le modèle d'apprentissage profond génératif pré-entraîné Transformer, les LLMs sont entraînés
sur de très grands ensembles de données, notamment des livres, des articles et des sites web. Les petits
modèles de langage (SLM – Small Language Model ) sont des modèles compacts avec moins de
paramètres que les grands modèles de langage, conçus pour fournir des solutions d'IA générative légères
et ciblées.
Les LLMs peuvent gérer les nuances linguistiques et générer un contenu cohérent. Deux concepts clés
aident les LLMs à traiter et à générer du contenu : la tokenisation et l'encodage appelé « embedding ». La
tokenisation et les embeddings convertissent le langage en une forme numérique que le modèle peut traiter
efficacement.

- La tokenisation dans les modèles de langage est le processus qui consiste à décomposer un texte
  en unités plus petites appelées tokens . Les tokens peuvent être aussi petits qu'un caractère ou
  aussi grands qu'un sous -mot ou un mot. Lorsqu'un LLM traite une phrase, il commence par
  tokeniser l'entrée afin que chaque token puisse être compris individuellement, tout en conservant
  le contexte global.
- Les embeddings sont des représentations numériques des tokens qui encodent leurs relations
  sémantiques, syntaxiques et contextuelles dans un format adapté au traitement par les modèles
  d'IA générative. Chaque token est transformé en un vecteur dans un espace à haute dimension,
  capturant des informations nuancées sur sa signification et son utilisation. Les tokens ayant des
  significations ou des rôles contextuels similaires ont des embeddings qui sont p ositionnés à
  proximité les uns des autres dans cet espace. Cette proximité permet aux LLM de comprendre les
  relations entre les mots, de conserver le contexte et de générer des réponses cohérentes et
  adaptées au contexte.
  Les LLMs utilisent une architecture de réseau neuronal connue sous le nom de modèle « Transformer ».
  Les modèles Transformer excellent dans les tâches linguistiques en traitant le contexte de longues
  séquences de texte et en apprenant comment les tokens sont liés les uns aux autres. Lors de l'inférence,
  les LLMs prédisent le token suivant dans une séquence, en tirant parti de ces relations apprises pour
  générer un texte cohérent et adapté au contexte. Le modèle Transformer peut être utilisé pour générer un
  nouveau texte statistiquement plausible, basé sur les données d'entraînement et la requête. Mais plausible
  ne signifie pas nécessairement correct.
  Les LLMs présentent un comportement non déterministe principalement dû à la nature probabiliste de leurs
  mécanismes d'inférence et à leurs configurations d'hyperparamètres. Ce comportement aléatoire inhérent
  peut entraîner des variations dans les résultats, même lorsque la même entrée est fournie plusieurs fois .
  Dans le domaine des LLMs, la fenêtre contextuelle fait référence à la quantité de texte au total, mesurée
  en tokens , que le modèle peut prendre en compte lors de la génération de réponses. Une fenêtre
  contextuelle plus grande permet au modèle de maintenir la cohérence sur des passages plus longs, par
  exemple lors de l'analyse de longs logs de test. Cependant, l'augment ation du nombre de tokens dans la
  fenêtre contextuelle augmente également la complexité de calcul et le temps de traitement nécessaires au
  modèle pour fonctionner efficacement.

Objectif d'apprentissage pratique HO -1.1.2 (H 1): Pratiquer la tokenisation et l'évaluation du
nombre de tokens
Cette activité pratique est conçue pour aider les candidats à acquérir une compréhension concrète de la
tokenisation et de ses implications lorsqu'ils travaillent avec des LLMs. L'exercice est divisé en deux
parties principales :

- Tokenisation : utilis ation d’un tokeniseur pour décomposer un échantillon de texte en tokens
  individuels. Examen du résultat pour voir comment les mots, la ponctuation et les phrases sont
  représentés, et identification des canevas ou des différences dans la tokenisation.
- Évaluation du nombre de tokens : mesure du nombre de tokens générés à partir de divers textes
  d'entrée. Analyse de l’influence du nombre de tokens sur les performances du modèle, en
  particulier en relation avec les limites de la fenêtre contextuelle du modèle et des considérations
  d'efficience.
  À la fin de cet exercice, les candidats seront en mesure de mieux anticiper comment différentes
  structures de texte et différentes longueurs d'entrée peuvent affecter les interactions avec les LLMs .

### 1.1.3 LLM de base, adapté aux instructions et de raisonnement

Les grands modèles de langage sont développés à travers des étapes d'entraînement et progressivement
spécialisés afin d'améliorer leur efficacité dans un large éventail de tâches. Ces étapes donnent lieu à trois
grandes catégories : LLM de fondation, LLM adapté aux instructions et LLM de raisonnement.

- LLM de fondation : Il s'agit de modèles polyvalents entraînés sur des ensembles de données vastes
  et diversifiés comprenant du texte, du code, des images et d'autres modalités. Leur pré -
  entraînement approfondi leur permet de prendre en charge diverses tâches dans des domaine s
  tels que le traitement du langage naturel, la vision par ordinateur et la reconnaissance vocale. Bien
  que puissants et flexibles, les modèles de fondation nécessitent généralement une adaptation
  supplémentaire pour répondre aux exigences spécifiques des requêtes à traiter .
- LLM adapté aux instructions : Dérivés des modèles de fondation, les LLMs adaptés aux instructions
  sont affinés à l'aide d'ensembles de données qui associent des requêtes à des réponses attendues.
  Cette étape améliore leur alignement avec les instructions humaines, ce qui renforce leur
  utilisabilité dans les applications du monde réel. Le processus d'ajustement consiste à optimiser le
  respect des tâches, le suivi des instructions et la cohérence des réponses, améliorant ainsi la
  capacité du modèle à interpréter et à agir efficacement selon l'intention de l'utilisateur.
- LLM de raisonnement : Les modèles de raisonnement étendent les modèles adaptés à des
  instructions en mettant l'accent sur les capacités cognitives structurées telles que l'inférence
  logique, la résolution de problèmes en plusieurs étapes et le raisonnement en chaîne. Ces modèles
  sont entraînés ou affinés à l'aide de tâches soigneusement sélectionnées qui exigent une
  compréhension contextuelle, des étapes de raisonnement intermédiaires et la synthèse
  d'informations complexes. Ils sont donc mieux adaptés aux tâches à forte charg e cognitive,
  notamment dans les domaines techniques.

Dans le contexte des applications d'IA générative pour les tests logiciels, on utilise à la fois des LLM
adaptés aux instructions (parfois appelés « non raisonnants ») et des LLM de raisonnement . Le choix
dépend de la complexité et des exigences en matière de raisonnement de la tâche de test spécifique à
accomplir.

### 1.1.4 LLM multimodaux et modèles de vision

Les LLM multimodaux étendent le modèle traditionnel du Transformer afin de traiter plusieurs modalités de
données, notamment le texte, les images, le son et la vidéo. Ces modèles sont entraînés sur des ensembles
de données volumineux et variés qui leur permettent d'apprendre les relations entre différents types de
données. Afin de gérer diverses modalités, la tokenisation est adaptée à chaque type de données. Par
exemple, les images sont converties en embeddings à l'aide de modèles de vision avant d'être traitées
dans le modèle Transformer.
Les modèles de vision, un sous -ensemble des LLM multimodaux, intègrent spécifiquement des
informations visuelles et textuelles pour effectuer des tâches telles que la légende d'images, la réponse à
des questions visuelles et l'analyse de la cohérence entre les entrées textuelles et visuelles .
Dans le domaine des tests logiciels, les LLM multimodaux, en particulier ceux enrichis d’un modèle de
vision, offrent des opportunités considérables. Ils peuvent analyser les éléments visuels des applications,
tels que les captures d'écran et les maquettes d'interface graphique, ainsi que les descri ptions textuelles
associées, telles que les rapports de défauts ou les User Stories. Cette capacité permet aux testeurs
d'identifier les divergences entre les résultats attendus et les éléments visuels réels sur une capture
d'écran. En outre, les LLM enrichis d’un modèle de vision peuvent générer des cas de test riches et réalistes
qui intègrent à la fois des données textuelles et des aspects visuels, augmentant ainsi la couverture globale.

Objectif d'apprentissage pratique HO-1.1.4 (H1) : Revue et exécution d'un prompt donné
adressant une tâche de test à l'aide d'un modèle LLM multimodal
Cet exercice consiste à examiner et à exécuter une requête donnée pour un LLM multimodal à l'aide
d'entrées textuelles et d'images afin de résoudre une tâche de test en deux étapes :

- Revoir les entrées : revue du prompt et des données d'entrée (texte et image).
- Exécution du prompt et vérification du résultat : utilisation d’un LLM multimodal pour traiter à la
  fois l'image et le texte, puis vérification de la réponse du LLM.
  Cet exercice montre comment s’utilisent les LLM multimodaux pour une tâche impliquant à la fois des
  entrées textuelles et visuelles , dans des cas d’usage de l’IA pour le test de logiciels, notamment en
  reconnaissant les avantages et les difficultés potentiels associés.

## 1.2 Tirer parti de l'IA générative dans les tests logiciels : principes généraux

L'IA générative offre des capacités transformatrices dans diverses activités de test. Les LLMs excellent
dans le traitement du langage naturel et du code, la génération de textes et de codes cohérents, la réponse

à des questions, la synthèse d'informations, la traduction de langues et l'analyse d'images dans un contexte
multimodal.
Les professionnels du test, quels que soit leurs rôles, peuvent tirer parti de l'IA générative de deux manières
complémentaires : grâce à des chatbots IA générative qui fournissent des réponses instantanées aux
prompts, et grâce à des applications basées sur les LLMs intégrés dans des outils de test .

### 1.2.1 Capacités clés des LLMs pour les tâches de test

Les LLMs peuvent interpréter les exigences, les spécifications, les captures d'écran, le code, les cas de
test et les rapports de défauts, ce qui en fait des outils permettant de traiter et de clarifier les informations
nécessaires tout au long du processus de test et de générer des éléments du testware. Voici quelques -
unes des principales capacités des LLMs pertinentes pour les tests logiciels :

- Analyse et amélioration des exigences : les LLMs peuvent aider à analyser les exigences et
  d'autres éléments de la base de test en identifiant les ambiguïtés, les incohérences ou les
  informations manquantes. Ils peuvent générer des questions pertinentes pour aider à clarifier les
  exigences lors des discussions avec les parties prenantes.
- Création de cas de test : les LLMs peuvent aider à générer des cas de test et suggérer des
  objectifs de test basés sur les exigences du système, les User Stories ou tout autre élément de la
  base de test.
- Génération d'oracles de test : les LLMs peuvent aider à générer les résultats attendus.
- Génération de données de test : les LLMs peuvent générer des ensembles de données, définir
  des valeurs limites et créer différentes combinaisons de données de test.
- Aide à l'automatisation des tests : les LLMs peuvent aider à générer des scripts de test à partir
  de la description des cas de test et améliorer les scripts de test existants en suggérant des
  modifications et en identifiant les techniques de conception des tests appropriées .
- Analyse des résultats des tests : les LLMs peuvent aider à analyser les résultats des tests en
  créant des résumés et en classant les anomalies en fonction de leur sévérité et de leur priorité .
- Création de testware : les LLMs peuvent aider à créer divers documents, notamment des plans
  de test, des rapports de test et des rapports de défauts, et à les mettre à jour au fur et à mesure
  de l'évolution du projet.
  Ces capacités montrent comment les LLMs peuvent avoir un impact sur divers aspects des tests logiciels
  tout au long du processus de test.

### 1.2.2 Chatbots IA et applications de test basées sur LLM pour les tests logiciels

Les chatbots IA et les applications de test basées sur LLM peuvent tous deux aider les testeurs, malgré
leurs différences en termes de fonctionnalités, de flexibilité et d'approches d'intégration .
Les chatbots IA offrent une interface conversationnelle conviviale qui permet aux testeurs de communiquer
directement avec les LLMs. Cette interaction en langage naturel permet aux testeurs d'entrer des
questions, des commandes ou des prompts et d'obtenir des réponses immédiates et contextuelles. Grâce
à des techniques telles que le chaînage de prompts, les testeurs peuvent affiner les résultats de manière

itérative, ce qui rend les chatbots particulièrement efficaces pour des tâches routinières, les tests
exploratoires et même l'intégration de nouveaux testeurs en leur fournissant un accès rapide aux
connaissances et aux pratiques en matière de test.
Ces chatbots IA sont particulièrement utiles dans les scénarios nécessitant un retour rapide, une
clarification des concepts de test ou une exploration dynamique des exigences et des cas de test potentiels.
Leur interface intuitive les rend accessibles même aux parties prenantes non techniques, élargissant ainsi
la base d'utilisateurs potentiels et encourageant une adoption large.
Les applications de test basées sur LLM , en revanche, impliquent l'intégration des capacités LLM via des
API afin d'effectuer des tâches de test bien définies et souvent automatisées. Ces applications offrent une
plus grande personnalisation et une plus grande évolutivité, permettant aux organisations et aux
fournisseurs d'outils d'intégrer l'IA générative dans l'outillage de test existants. Cela permet l'automatisation
de tâches répétitives ou complexes, telles que la génération de cas de test , l'analyse des défauts ou la
synthèse des données de test. Dans des implémentations plus avancées, les organisations peuvent créer
des agents IA spécialement conçus pour remplir certaines fonctions de test (voir chapitre 4) .
Quelle que soit la manière dont le testeur interagit avec les LLMs, que ce soit via des chatbots ou des
applications intégrées basées sur LLM, la mise en œuvre réussie de l'IA générative dans les tests nécessite
une ingénierie de requêtes efficace (voir chapitre 2). Des requêtes soigneusement conçues et des
instructions claires et spécifiques sont essentielles pour garantir que les résultats générés par les LLM sont
précis, pertinents et alignés sur les objectifs des tests. Cette pratique permet de maximiser la valeur tirée
de l'IA générative et garantit un soutien cohérent et fiable pour un large éventail d'activités de test .
