===========================================================================
CHAPITRE 5 — DÉPLOIEMENT & INTÉGRATION
===========================================================================

===========================================================================
SECTION: intro — Vue d'ensemble du chapitre
===========================================================================
Le chapitre 5 traite de l'intégration concrète de la GenAI dans une organisation de test : les risques de l'IA fantôme, la stratégie de déploiement, la sélection des modèles, les phases d'adoption, les compétences nécessaires et l'évolution des rôles. 
===========================================================================
SECTION: s511 — 5.1.1 Shadow AI
===========================================================================
🎯 GenAI-5.1.1 (K1) — Rappeler les risques liés à l'IA fantôme
L'**IA fantôme** (Shadow AI) désigne l'utilisation non contrôlée d'outils d'IA par les équipes, sans gouvernance ni approbation de l'organisation. Elle entraîne 3 catégories de risques :
📊 Risque | Description
  | Sécurité et confidentialité | Les outils d'IA personnels peuvent présenter des lacunes de sécurité → violations de données |
  | Conformité et réglementaire | Utiliser des outils non approuvés peut entraîner la non-conformité aux normes/réglementations (EU AI Act, RGPD) → conséquences juridiques |
  | Propriété intellectuelle | Accords de licence flous → litiges en matière de PI, surtout si des données protégées par le droit d'auteur sont traitées sans autorisation |
📌 Point clé: Une **stratégie et des étapes formelles** pour l'intégration de la GenAI aident les
 organisations à **éviter les risques de l'IA fantôme**. C'est la raison d'être de
 tout ce chapitre.
📌 Mot-clé examen: Mots-clés: IA fantôme (Shadow AI)

===========================================================================
SECTION: s512 — 5.1.2 Stratégie GenAI
===========================================================================
🎯 GenAI-5.1.2 (K2) — Expliquer les aspects clés d'une stratégie GenAI
Pour une intégration réussie, **6 facteurs clés** à examiner :
📊 N° | Facteur | Description
  | 1 | Objectifs mesurables | Définir des objectifs clairs : augmenter la productivité, raccourcir les cycles de test, améliorer la qualité |
  | 2 | Choix du LLM | Aligné sur les objectifs de test, compatible avec l'infra existante, répondant aux exigences de scalabilité (cf. 5.1.3) |
  | 3 | Qualité des données | L'efficacité dépend de données d'entrée précises et pertinentes, protégées par des procédures de sécurité robustes |
  | 4 | Formation | Programmes complets pour les compétences techniques ET éthiques nécessaires |
  | 5 | Métriques | Collecter des métriques spécifiques pour mesurer l'efficacité des résultats GenAI (cf. section 2.3.1) |
  | 6 | Conformité et éthique | Directives d'utilisation : règles sur les données sensibles, obligations de transparence, contrôles qualité avec revue des testware générés |
📌 Point examen: La **transparence** est explicitement mentionnée : l'organisation doit indiquer 
 **ce qui a été généré par l'IA**. Et les testware générés doivent faire l'objet d'un 
 **contrôle qualité avec revue**.

===========================================================================
SECTION: s513 — 5.1.3 Sélection des LLMs
===========================================================================
🎯 GenAI-5.1.3 (K2) — Résumer les critères de sélection des LLMs/SLMs
Il existe peu de benchmarks spécifiquement axés sur les tâches de test logiciel. La sélection nécessite **4 critères clés** :
📊 Critère | Description
  | Performances du modèle | Évaluer sur les tâches de test ciblées par rapport aux benchmarks de l'organisation, avec les métriques de la section 2.3.1 |
  | Potentiel de fine-tuning | Évaluer s'il est possible et utile d'affiner le modèle avec des données spécifiques au domaine pour augmenter la précision |
  | Coût récurrent | Licence + dépenses opérationnelles. S'assurer que les coûts correspondent au budget pour les tâches ciblées. |
  | Communauté et support | Choisir des modèles avec communauté active et documentation détaillée pour faciliter l'implémentation |
📌 Exercice pratique HO-5.1.3 (H1): Estimer les coûts récurrents pour une tâche de test donnée : nombre de tokens
 entrée/sortie, fréquence de la tâche, comparaison des modèles de tarification (au moins
 1 commercial + 1 open source).

===========================================================================
SECTION: s514 — 5.1.4 Phases d'adoption
===========================================================================
🎯 GenAI-5.1.4 (K1) — Rappeler les phases d'adoption
📌 Points clés: Ces phases peuvent se dérouler **en parallèle** pour différents cas d'usage (ex:
 l'analyse de rapports avancée alors que l'automatisation en est aux débuts).
 Le syllabus mentionne aussi l'importance de 
 **traiter les craintes de perte d'emploi** qui peuvent impacter l'adoption et le
 moral de l'équipe.

===========================================================================
SECTION: s521 — 5.2.1 Compétences essentielles
===========================================================================
🎯 GenAI-5.2.1 (K2) — Compétences essentielles pour tester avec la GenAI

**Compétences techniques**
  • Maîtrise des **techniques d'ingénierie du prompting**
  • Compréhension des **fenêtres contextuelles** des modèles
  • Développement de **méthodes de revue** des testware générés
  • Évaluation des **capacités des LLMs** et des techniques d'amélioration des prompts
  • Combinaison de l'**expertise domaine/test** avec les compétences IA

**Connaissances des risques**
  • Comprendre les **risques inhérents** à la GenAI et les stratégies d'atténuation
  • Comprendre les implications de **sécurité des données** du partage de testware avec les LLMs
  • Implémenter l'**expurgation des données** (suppression/masquage des informations sensibles)
  • Suivre les pratiques de prompting **préservant la confidentialité**

**Considérations environnementales**
  • Optimiser la **sélection des modèles** pour réduire la charge informatique
  • Équilibrer les **avantages de l'automatisation** avec l' **impact sur les coûts et l'énergie**

===========================================================================
SECTION: s522 — 5.2.2 Développer les capacités
===========================================================================
🎯 GenAI-5.2.2 (K1) — Stratégies pour développer les compétences IA

**Approche de montée en compétences**
  • **Pratique avec divers LLMs/SLMs** — expérimenter plusieurs modèles
  • **Parcours d'apprentissage structurés** — du basique au ciblé
  • **Partage de savoir-faire** au sein de l'organisation
  • **Exercices guidés** et apprentissage entre pairs (peer learning)
  • **Intégration progressive** de l'IA dans les tâches quotidiennes

**Progression des compétences**
Les testeurs passent de la création de **prompts de base** à l'utilisation de techniques plus ciblées avec des **canevas de prompt** (templates réutilisables pour des résultats cohérents et fiables).

**Communautés de pratique internes**
  • Réunions régulières pour partager les **applications réussies**
  • Discussion des **défis** rencontrés
  • Partage de **bibliothèques de canevas de prompts**
  • Documentation des **leçons tirées** par projet et domaine
📌 Définition à retenir: Un **canevas de prompt** (prompt template) = un template réutilisable pour créer des
 prompts efficaces, guidant l'IA vers des résultats cohérents et fiables.

===========================================================================
SECTION: s523 — 5.2.3 Évolution des rôles
===========================================================================
🎯 GenAI-5.2.3 (K1) — Évolution des processus et responsabilités
L'intégration de la GenAI transforme les rôles traditionnels :
📊 Rôle | Avant GenAI | Avec GenAI
  | Testeurs | Spécialistes de la conception et de l'exécution des tests | Spécialistes des tests assistés par l'IA : guider et vérifier les testware générés, remanier les prompts, maintenir les bibliothèques de prompts |
  | Test managers | Gestion des équipes et des processus de test | En plus : stratégie de test basée sur l'IA, gestion des risques IA, supervision d'équipes hybrides humains + agents IA, cadres de gouvernance IA |
📌 Points clés pour l'examen: Les testeurs ne perdent pas leurs **compétences traditionnelles** — ils les combinent
 avec des compétences IA. Le test manager doit coordonner des **équipes hybrides** 
 (humains + agents IA). Les deux rôles évoluent, aucun n'est supprimé.
📌 Nouvelles tâches du testeur: Revue des résultats basés sur l'IA + remaniement des prompts + maintenance des
 bibliothèques de prompts spécifiques aux tests. La revue humaine reste 
 **indispensable**.