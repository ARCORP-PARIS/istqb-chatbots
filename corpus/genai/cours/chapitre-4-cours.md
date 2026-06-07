===========================================================================
CHAPITRE 4 — INFRASTRUCTURE LLM
===========================================================================
Le chapitre 4 couvre les briques techniques pour industrialiser la GenAI dans les tests : architecture, RAG, agents IA, fine-tuning et LLMOps. 
===========================================================================
SECTION: s411 — 4.1.1 Composants architecturaux d'un système basé LLM
===========================================================================
🎯 GenAI-4.1.1 (K2) — Expliquer les composants architecturaux
Une infrastructure de test basée sur LLM intègre un LLM dans le processus de test pour améliorer l'automatisation, le raisonnement et la prise de décision. Elle se compose de **3 couches** :
📊 Couche | Rôle | Détails
  | Front-end | Interface utilisateur | Les testeurs saisissent des requêtes ou commandes. C'est le point d'entrée. |
  | Back-end | Traitement et orchestration | Gère l'authentification, la récupération de données, la préparation des prompts, l'interaction avec le LLM et le post-traitement des résultats. |
  | LLM | Moteur intelligent | Hébergé en service tiers (via API) ou en modèle interne. Génère les réponses à partir de prompts structurés. |

**Ce qui distingue cette architecture d'un simple chatbot**
  • Le LLM n'est pas un simple serveur mais un **composant de traitement intelligent** qui interprète et raisonne
  • L'infrastructure génère des informations de test **dynamiquement à partir du contexte** (exigences, code, résultats) — pas de réponses scriptées
  • Le back-end intègre **plusieurs sources de données** : bases relationnelles (données structurées, cas de test) et bases vectorielles (recherche sémantique via embeddings)
  • Le back-end fait du **post-traitement** pour s'assurer que les résultats correspondent aux conditions de test
📌 Mots-clés à retenir: Mots-clés: infrastructure de test, base de données vectorielle, front-end, back-end, post-traitement

===========================================================================
SECTION: s412 — 4.1.2 RAG (Retrieval-Augmented Generation)
===========================================================================
🎯 GenAI-4.1.2 (K2) — Résumer les principes du RAG
Le RAG améliore les LLMs en intégrant des **sources de données externes** dans le processus de génération, augmentant la pertinence et la précision des résultats.

**Phase de préparation (indexation)**
🔄 Flux: Documents volumineux → Découpage en fragments (256-512 tokens) → Nettoyage et traitement → Encodage en embeddings → Stockage en base vectorielle

**Phase d'utilisation (inférence) — 2 étapes**
📊 Étape | Description
  | 1. Récupération (Retrieval) | Le prompt utilisateur est encodé en embedding. Le système récupère les fragments les plus pertinents de la base vectorielle par similarité sémantique. |
  | 2. Génération (Generation) | Les fragments récupérés sont transmis au LLM comme contexte. Le LLM combine ses connaissances + les données récupérées pour générer une réponse fondée et contextualisée. |

**Application dans les tests logiciels**
Le RAG permet à l'infrastructure de test d'accéder aux **sources de données de l'entreprise** (bases de données, documentation, référentiels) en temps réel. Les tâches d'analyse et de conception de test sont ainsi alignées sur les **dernières spécifications, exigences et données de test existantes**.
📌 Pourquoi le RAG est crucial: Le RAG résout le problème fondamental des LLMs : leurs connaissances sont figées à la
 date d'entraînement. Avec le RAG, le LLM accède à des données 
 **actuelles et spécifiques au projet**, ce qui réduit les hallucinations et améliore
 la pertinence.
📌 Exercice pratique HO-4.1.2 (H1): Expérimenter un système RAG : intégrer des documents, comparer les résultats du LLM 
 **avec et sans RAG** pour une tâche de test. Identifier forces et limites.

===========================================================================
SECTION: s413 — 4.1.3 Agents LLM
===========================================================================
🎯 GenAI-4.1.3 (K2) — Expliquer le rôle des agents basés sur LLM
Les agents LLM sont des applications GenAI spécialisées pour le **traitement semi-autonome ou autonome** de tâches. Contrairement aux chatbots (question-réponse), les agents peuvent **« agir »** en invoquant des **outils** (fonctions prédéfinies) et interagir avec des systèmes externes.

**Deux niveaux d'autonomie**
📊 Type | Description | Supervision
  | Agents autonomes | Exécutent indépendamment avec règles prédéfinies, apprentissage par renforcement et boucles de rétroaction adaptatives | Intervention humaine minimale |
  | Agents semi-autonomes | Exécutent sous supervision périodique pour garantir l'alignement avec les objectifs définis par l'utilisateur | Supervision humaine régulière |

**Architectures multi-agents**
Système collaboratif où **plusieurs agents spécialisés** communiquent et se coordonnent pour résoudre des problèmes complexes plus efficacement qu'un seul agent. Cet effort coordonné s'appelle l'**orchestration**.
📌 Risques des agents: Les agents souffrent des **mêmes problèmes** que les LLMs : hallucinations, erreurs
 de raisonnement, biais. Atténuation : procédures de **vérification automatisées** ou
 utilisation d'**agents semi-autonomes** pour les tâches critiques.
📌 Point examen — Chatbot vs Agent: **Chatbot IA** = interaction question-réponse conversationnelle.
 **Agent LLM** = peut agir, invoquer des outils, interagir avec des systèmes externes,
 fonctionner de manière (semi-)autonome.

===========================================================================
SECTION: s421 — 4.2.1 Fine-tuning
===========================================================================
🎯 GenAI-4.2.1 (K2) — Expliquer le fine-tuning pour les tâches de test
Le fine-tuning adapte un modèle pré-entraîné (LLM ou SLM) pour des **tâches spécifiques** ou des **domaines particuliers**. On poursuit l'entraînement sur un ensemble de données ciblé pour acquérir des connaissances spécifiques au domaine.

**Pourquoi faire du fine-tuning ?**
  • Doter un LLM générique de **capacités de raisonnement spécialisées** pour un domaine
  • Adopter un **vocabulaire propre** au domaine
  • Générer des résultats dans un **format spécifique à l'organisation**
📌 Exemple concret: Fine-tuner un LLM sur les User Stories de l'organisation et les cas de test
 correspondants → le modèle s'aligne sur le 
 **processus de test et la terminologie spécifiques** de l'entreprise.

**Fine-tuning sur SLM vs LLM**
Le fine-tuning peut aussi s'appliquer aux **SLMs** (Small Language Models), moins gourmands en ressources. Un SLM affiné peut atteindre des performances élevées sur des tâches spécifiques **sans la charge informatique d'un LLM**.

**4 défis du fine-tuning**
📊 Défi | Description
  | Données de qualité | Éviter les résultats biaisés/inexacts → utiliser des ensembles d'entraînement de haute qualité et spécifiques à la tâche |
  | Surajustement (overfitting) | Le modèle devient trop spécialisé → mauvaises performances sur des données nouvelles. Maintenir la généralisation. |
  | Opacité | Manque de transparence dans les décisions du LLM → complique le débogage et la validation |
  | Ressources informatiques | Le fine-tuning des LLMs nécessite des ressources significatives (moins pour les SLMs) |

===========================================================================
SECTION: s422 — 4.2.2 LLMOps
===========================================================================
🎯 GenAI-4.2.2 (K2) — Expliquer les LLMOps
**LLMOps** (Large Language Model Operations) = ensemble des pratiques, outils et processus pour le développement, le déploiement et la maintenance des LLMs en production.

**3 approches d'utilisation (non exclusives)**
📊 Approche | Description | Considérations clés
  | Chatbot IA | Utiliser un chatbot IA existant (LLM-as-a-Service ou infra interne open source) | Confidentialité, sécurité, coûts. Auditer les garanties du fournisseur. |
  | Outil de test avec GenAI | Utiliser un outil de test du marché doté de capacités GenAI intégrées | Mêmes enjeux + évaluer les garanties de sécurité et performance du fournisseur. Analyse coûts-avantages. |
  | Développement interne | Développer en interne un outil de test basé sur GenAI | Contrôle total sur la confidentialité. Coûts d'exploitation (compute, stockage, formation). Expertise requise en implémentation LLM. |
📌 Points clés pour l'examen: Ces 3 approches **ne s'excluent pas mutuellement** — une organisation peut les
 combiner selon les tâches. Elles peuvent toutes intégrer du **RAG** et du 
 **fine-tuning** pour améliorer les résultats.
📌 Piège QCM: Ne confonds pas **fine-tuning** (adapter le modèle en poursuivant l'entraînement) et 
 **RAG** (enrichir les réponses avec des données externes sans modifier le modèle). Le
 fine-tuning change le modèle, le RAG ne le change pas.