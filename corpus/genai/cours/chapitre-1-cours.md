CHAPITRE 1 — INTRODUCTION À L'IA GÉNÉRATIVE POUR LES TESTS LOGICIELS

==========================================
1.1.1 PANORAMA DE L'IA
==========================================
[LO] GenAI-1.1.1 (K1) — Rappeler les différents types d'IA

L'intelligence artificielle englobe plusieurs familles de technologies, chacune
avec sa propre logique. Le syllabus en identifie quatre :

| Type d'IA           | Principe                                                                                              | Exemple en test                                                |
| IA symbolique       | Système basé sur des règles logiques et des symboles pour imiter la prise de décision humaine.        | Systèmes experts, arbres de décision codés manuellement        |
| ML classique        | Approche basée sur les données : préparation, sélection de features, entraînement de modèles.         | Catégorisation des défauts, prédiction de zones à risque       |
| Deep Learning       | Réseaux neuronaux qui apprennent automatiquement les features à partir de données massives.           | Reconnaissance d'éléments UI dans les captures d'écran         |
| IA Générative       | Deep learning pour créer du nouveau contenu (texte, images, code) en imitant les patterns appris.     | Génération de cas de test, scripts d'automatisation, data synthétiques |

★ POINT CLÉ POUR L'EXAMEN
L'avantage principal de l'IA générative pour le test : elle utilise des MODÈLES
PRÉ-ENTRAÎNÉS applicables directement aux tâches de test SANS PHASE
D'ENTRAÎNEMENT SUPPLÉMENTAIRE. Mais cela comporte des risques (hallucinations,
biais — voir chapitre 3).

CE QU'ON PEUT VOUS DEMANDER
Identifier quel type d'IA correspond à quelle description.
Exemple : « Un système qui utilise des règles logiques prédéfinies pour prendre
des décisions » → IA symbolique.


==========================================
1.1.2 BASES GENAI & LLMs
==========================================
[LO] GenAI-1.1.2 (K2) — Expliquer les bases de l'IA générative et des LLMs

Les LLMs (Large Language Models) sont basés sur l'architecture TRANSFORMER
(modèle génératif pré-entraîné). Ils sont entraînés sur d'immenses ensembles
de données : livres, articles, sites web.

TOKENISATION
C'est le processus de décomposition d'un texte en unités plus petites appelées
TOKENS. Un token peut être un caractère, un sous-mot ou un mot entier. Le LLM
tokenise l'entrée avant de la traiter.

EMBEDDINGS
Ce sont des REPRÉSENTATIONS NUMÉRIQUES (VECTEURS) des tokens qui capturent leurs
relations sémantiques, syntaxiques et contextuelles. Les tokens ayant des
significations similaires ont des embeddings proches dans l'espace vectoriel.
C'est ce qui permet au LLM de « comprendre » le sens.

ARCHITECTURE TRANSFORMER
Les Transformers traitent le contexte de longues séquences de texte et
apprennent les relations entre tokens. Lors de l'inférence, le LLM PRÉDIT LE
TOKEN SUIVANT dans la séquence.

⚠ PHRASE CLÉ DU SYLLABUS
« Le modèle Transformer peut générer un nouveau texte STATISTIQUEMENT PLAUSIBLE.
Mais PLAUSIBLE NE SIGNIFIE PAS NÉCESSAIREMENT CORRECT. » — C'est la source des
hallucinations.

COMPORTEMENT NON DÉTERMINISTE
Les LLMs sont NON DÉTERMINISTES : la même entrée peut produire des résultats
différents à chaque exécution. Cela est dû à la nature probabiliste de
l'inférence et aux configurations d'hyperparamètres (comme la température).

FENÊTRE CONTEXTUELLE
C'est la quantité totale de texte (en tokens) que le modèle peut prendre en
compte lors de la génération. Une fenêtre plus grande = meilleure cohérence
sur de longs textes, mais plus de coût de calcul.

SLM — SMALL LANGUAGE MODELS
Modèles compacts avec moins de paramètres, conçus pour des solutions GenAI
légères et ciblées.

MOTS-CLÉS À RETENIR
tokenisation • embedding • Transformer • fenêtre contextuelle • non déterministe
• token • SLM

EXERCICE PRATIQUE HO-1.1.2 (H1)
Pratiquer la tokenisation : utiliser un tokeniseur (ex : celui d'OpenAI) pour
décomposer un texte en tokens, observer comment les mots et la ponctuation sont
représentés, puis mesurer le nombre de tokens pour évaluer l'impact sur la
fenêtre contextuelle.


==========================================
1.1.3 TYPES DE LLMs
==========================================
[LO] GenAI-1.1.3 (K2) — Différencier LLM de base, adapté aux instructions et de raisonnement

Les LLMs passent par des étapes d'entraînement progressif, ce qui donne lieu à
3 catégories :

| Type                          | Description                                                                                                                        | Quand l'utiliser                                          |
| LLM de fondation              | Modèle polyvalent pré-entraîné sur des données massives (texte, code, images). Puissant mais nécessite une adaptation pour des tâches spécifiques. | Base pour construire des modèles spécialisés              |
| LLM adapté aux instructions   | Affiné avec des paires requête/réponse pour mieux suivre les instructions humaines. Améliore suivi des consignes et cohérence.     | Tâches de test standard, chatbots IA, usage quotidien     |
| LLM de raisonnement           | Spécialisé dans l'inférence logique, la résolution multi-étapes et le raisonnement en chaîne. Meilleur pour contexte complexe.     | Tâches à forte charge cognitive : analyse d'impact, tests complexes |

★ POINT CLÉ POUR L'EXAMEN
Le choix entre LLM adapté aux instructions (« non raisonnant ») et LLM de
raisonnement dépend de la COMPLEXITÉ et des EXIGENCES DE RAISONNEMENT de la
tâche de test. Les deux sont utilisés dans le contexte des tests logiciels.


==========================================
1.1.4 MULTIMODAL & VISION
==========================================
[LO] GenAI-1.1.4 (K2) — Résumer les principes des modèles multimodaux et de vision

LLM MULTIMODAUX
Ils étendent le Transformer pour traiter PLUSIEURS MODALITÉS DE DONNÉES : texte,
images, son, vidéo. La tokenisation est adaptée à chaque type de données — par
exemple, les images sont converties en embeddings via des modèles de vision
avant d'être traitées par le Transformer.

MODÈLES DE VISION
Sous-ensemble des LLM multimodaux qui intègrent spécifiquement des INFORMATIONS
VISUELLES ET TEXTUELLES. Ils peuvent :
- Légender des images
- Répondre à des questions visuelles
- Analyser la cohérence entre texte et éléments visuels

APPLICATIONS POUR LE TEST LOGICIEL
- Analyser les captures d'écran et maquettes d'interface graphique
- Identifier les divergences entre résultats attendus et éléments visuels réels
- Générer des cas de test intégrant à la fois des données textuelles et visuelles
- Croiser rapports de défauts textuels avec captures d'écran

EXERCICE PRATIQUE HO-1.1.4 (H1)
Prompt multimodal : Examiner et exécuter un prompt donné pour un LLM multimodal
utilisant texte + image pour une tâche de test. En deux étapes : (1) revue des
entrées, (2) exécution et vérification du résultat.


==========================================
1.2.1 CAPACITÉS CLÉS DES LLMs POUR LE TEST
==========================================
[LO] GenAI-1.2.1 (K2) — Donner des exemples de capacités clés des LLMs pour les tâches de test

Les LLMs peuvent interpréter des exigences, des spécifications, des captures
d'écran, du code, des cas de test et des rapports de défauts. Voici les
7 CAPACITÉS CLÉS identifiées par le syllabus :

| N° | Capacité                              | Description                                                                                          |
| 1  | Analyse et amélioration des exigences | Identifier ambiguïtés, incohérences, informations manquantes. Générer des questions pour clarifier.   |
| 2  | Création de cas de test               | Générer des cas de test et objectifs de test à partir des User Stories et exigences.                  |
| 3  | Génération d'oracles de test          | Générer les résultats attendus pour les cas de test.                                                  |
| 4  | Génération de données de test         | Créer des jeux de données, valeurs limites, combinaisons de données.                                  |
| 5  | Aide à l'automatisation               | Générer des scripts de test, suggérer des modifications, identifier les techniques appropriées.       |
| 6  | Analyse des résultats                 | Résumer les résultats, classer les anomalies par sévérité et priorité.                                |
| 7  | Création de testware                  | Créer / mettre à jour plans de test, rapports de test, rapports de défauts.                           |

ASTUCE MÉMORISATION
Retiens l'acronyme ACGGA-AC : Analyse, Cas de test, Génération oracles,
Génération données, Automatisation, Analyse résultats, Création testware.
Ces 7 capacités couvrent tout le processus de test.


==========================================
1.2.2 CHATBOTS vs APPLICATIONS BASÉES SUR LLM
==========================================
[LO] GenAI-1.2.2 (K2) — Comparer les modalités d'interaction avec la GenAI

Deux façons complémentaires d'utiliser l'IA générative pour les tests :

| Critère        | Chatbots IA                                                                       | Applications basées sur LLM                                            |
| Interface      | Conversationnelle en langage naturel                                              | Intégration via API dans les outils existants                          |
| Flexibilité    | Très flexible, interaction dynamique                                              | Personnalisation poussée, tâches bien définies                         |
| Cas d'usage    | Feedback rapide, tests exploratoires, onboarding de testeurs, clarification       | Automatisation à grande échelle, génération de cas, analyse de défauts, agents IA |
| Utilisateurs   | Accessible même aux non-techniques                                                | Nécessite des compétences techniques d'intégration                     |
| Scalabilité    | Usage individuel / petit groupe                                                   | Scalable à l'organisation entière                                      |
| Technique clé  | Chaînage de prompts pour affiner les résultats itérativement                      | Agents IA spécialisés pour des fonctions de test (cf. chapitre 4)      |

★ POINT CLÉ POUR L'EXAMEN
Quelle que soit la modalité (chatbot ou application intégrée), la mise en œuvre
réussie de l'IA générative nécessite une INGÉNIERIE DE PROMPTS EFFICACE.
Des prompts soigneusement conçus sont essentiels pour garantir des résultats
précis, pertinents et alignés sur les objectifs de test.

===========================================================================
FIN DU CHAPITRE 1
===========================================================================
