===========================================================================
CHAPITRE 2 — INGÉNIERIE DU PROMPTING
===========================================================================

Le chapitre 2 couvre l'ingénierie du prompting — de la structure des prompts à leur application concrète à chaque activité de test, puis l'évaluation et l'affinage des résultats.
===========================================================================
SECTION: s211 — 2.1.1 Structure des prompts (6 composants RCIDCF)
===========================================================================
🎯 GenAI-2.1.1 (K2) — Donner des exemples de la structure des prompts
Un prompt structuré pour le test logiciel comprend 6 composants . Chacun contribue à la clarté et à la précision de la communication avec le LLM.
📊 N° | Composant | Rôle | Exemple
  | 1 | Rôle | Perspective ou persona du LLM | « Tu es un testeur QA senior spécialisé en tests fonctionnels » |
  | 2 | Contexte | Infos de base sur l'objet de test | « Application bancaire mobile, sprint 12, module paiements » |
  | 3 | Instructions | Directives claires décrivant la tâche | « Génère des cas de test couvrant les scénarios positifs et négatifs » |
  | 4 | Données d'entrée | US, critères, captures, code, cas existants | La User Story avec ses critères d'acceptation |
  | 5 | Contraintes | Restrictions et considérations | « Respecte le RGPD, ne génère pas de données personnelles réelles » |
  | 6 | Format de sortie | Structure/format attendu de la réponse | « Format Gherkin Given-When-Then, en français » |
📌 Aide-mémoire: Retiens R-C-I-D-C-F : Rôle, Contexte, Instructions, Données d'entrée, Contraintes, Format. Cette structure doit être combinée avec les techniques de prompting (section suivante).

===========================================================================
SECTION: s212 — 2.1.2 Techniques de prompting (Enchaînement, Few-shot, Méta-prompting)
===========================================================================
🎯 GenAI-2.1.2 (K2) — Différencier les principales techniques de prompting
Le syllabus identifie 3 techniques majeures à combiner avec la structure en 6 composants :

**1. Enchaînement de prompts (Prompt Chaining)**
Diviser une tâche complexe en plusieurs prompts séquentiels . Le résultat de chaque étape est vérifié (manuellement ou automatiquement) et remanié avant de passer à l'étape suivante.
  • Chaque réponse informe le prompt suivant → plus grande précision
  • Décomposition en sous-tâches avec vérification systématique
  • Permet des interactions dynamiques
📌 Exemple concret: Prompt 1 : « Analyse cette User Story et identifie les ambiguïtés » → vérification humaine Prompt 2 : « Génère des conditions de test basées sur l'analyse précédente » → vérification Prompt 3 : « Crée des cas de test détaillés pour chaque condition » → validation finale

**2. Few-shot prompting**
Fournir des exemples dans le prompt pour guider le modèle. Trois variantes :
📊 Variante | Nombre d'exemples | Usage
  | Zero-shot | 0 exemple | Le LLM utilise ses connaissances pré-entraînées |
  | One-shot | 1 exemple | Un seul exemple pour illustrer le format attendu |
  | Few-shot | Plusieurs exemples | Plusieurs exemples pour guider vers le résultat souhaité |
Particulièrement efficace pour les tâches avec un format de sortie contraint (ex: Gherkin, keyword-driven).

**3. Méta-prompting**
Exploiter la capacité du LLM à générer ou remanier ses propres prompts . Le testeur demande au LLM de créer un prompt optimisé, l'évalue et l'affine itérativement.
  • Forme de « binôme testeur-IA » (pair testing)
  • Réduit l'effort manuel de conception des prompts
  • Utile quand on ne sait pas comment créer un prompt efficace
📌 Combinaison des techniques: Les 3 techniques se combinent . Exemple : méta-prompting pour créer le prompt initial → few-shot pour ajouter des exemples → enchaînement pour valider étape par étape.
📌 Piège examen: Ne confonds pas enchaînement de prompts (plusieurs prompts séquentiels avec vérification) et few-shot prompting (exemples dans un seul prompt). L'enchaînement = multi-prompts. Le few-shot = un seul prompt avec exemples.

===========================================================================
SECTION: s213 — 2.1.3 Prompt système vs Prompt utilisateur
===========================================================================
🎯 GenAI-2.1.3 (K2) — Distinguer prompts système et utilisateur
📊 Critère | Prompt système | Prompt utilisateur
  | Défini par | Développeur / testeur | Utilisateur du chatbot |
  | Visibilité | Non visible dans la conversation | Visible dans la conversation |
  | Fréquence | Défini une seule fois au début de la session | Change à chaque interaction |
  | Contenu | Comportement global, ton, règles du domaine | Question ou tâche spécifique |
  | Composants RCIDCF | Rôle, Contexte, Contraintes | Instructions, Données d'entrée, Format de sortie |
📌 Exemple concret: Prompt système : « Tu es un assistant QA ISTQB. Réponds en langage formel. Concentre-toi sur les bonnes pratiques. Évite les spéculations. » Prompt utilisateur : « Énumère les différences entre les tests boîte noire et boîte blanche avec des exemples. »
  ` « Tu es un assistant QA ISTQB. Réponds en langage formel. Concentre-toi sur les bonnes pratiques. Évite les spéculations. » `
  ` « Énumère les différences entre les tests boîte noire et boîte blanche avec des exemples. » `
📌 Point clé: Le LLM génère ses réponses en tenant compte des deux : le prompt système (cadre permanent) + le prompt utilisateur (question immédiate). Le prompt système agit comme un filtre permanent sur toutes les réponses.

===========================================================================
SECTION: s221 — 2.2.1 Application à l'analyse de test
===========================================================================
🎯 GenAI-2.2.1 (K3) — Appliquer l'IA générative aux tâches d'analyse de test
Entrées : exigences, User Stories, spécifications techniques, maquettes IHM. Sortie : conditions de test, identification de défauts, recommandations.

**5 tâches d'analyse de test supportées par la GenAI**
📊 N° | Tâche | Description
  | 1 | Identifier les défauts dans la base de test | Détecter incohérences, ambiguïtés et informations incomplètes dans les exigences |
  | 2 | Générer des conditions de test | Transformer les User Stories en conditions de test structurées |
  | 3 | Hiérarchiser par risque | Évaluer la probabilité, l'impact, la conformité réglementaire et l'historique des défauts |
  | 4 | Analyse de couverture | Cartographier exigences → conditions de test pour vérifier que rien n'est oublié |
  | 5 | Suggérer des techniques de test | Recommander des techniques appropriées : valeurs limites, partitions d'équivalence, tables de décision |
📌 Attention: La qualité des entrées conditionne directement l'exactitude des résultats. Des données d'entrée mal structurées ou incomplètes → des résultats médiocres du LLM.
📌 Exercices pratiques: HO-2.2.1a (H2) — Créer des prompts multimodaux (texte + maquette IHM) pour générer des critères d'acceptation. HO-2.2.1b (H2) — Utiliser des prompts pour dériver des conditions de test à partir de User Stories.

===========================================================================
SECTION: s222 — 2.2.2 Conception et implémentation des tests
===========================================================================
🎯 GenAI-2.2.2 (K3) — Appliquer l'IA générative à la conception et l'implémentation des tests

**4 tâches clés**
📊 Tâche | Description
  | Génération de cas de test | Préconditions, entrées, résultats attendus, couverture des exigences |
  | Synthèse de données de test | Données synthétiques, représentatives, respectueuses de la confidentialité, couvrant les cas aux limites |
  | Génération de scripts automatisés | Code compatible avec les frameworks d'automatisation (Selenium, Playwright, Cypress, etc.) |
  | Planification et priorisation | Identifier les interdépendances entre les cas de test et proposer un calendrier d'exécution optimal |
📌 Exercices pratiques: HO-2.2.2a (H2) — Générer des cas de test fonctionnels en 3 étapes : (1) prompt structuré → (2) vérification couverture via tableau → (3) méta-prompt pour tests E2E. HO-2.2.2b (H1) — Comparer les résultats d'au moins 2 LLMs sur la même tâche de génération de scripts.

===========================================================================
SECTION: s223 — 2.2.3 Tests de régression automatisés
===========================================================================
🎯 GenAI-2.2.3 (K3) — Appliquer l'IA générative aux tests de régression automatisés
Le nombre de cas de test de régression augmente à chaque itération/release, ce qui en fait des candidats idéaux pour l'automatisation, en particulier dans les pipelines CI/CD (intégration continue / livraison continue). La GenAI peut rationaliser la création, la maintenance et l'optimisation des suites de régression en s'adaptant dynamiquement aux modifications du code.

**5 activités de régression supportées par la GenAI**
📊 Activité | Description
  | Scripts keyword-driven | Implémenter des scripts basés sur des mots-clés prédéfinis représentant des étapes de test courantes |
  | Analyse d'impact | Analyser les modifications de code pour identifier les zones à haut risque et cibler la régression |
  | Tests auto-réparateurs (self-healing) | Ajuster automatiquement les scripts pour gérer les changements mineurs d'UI/API (localisateurs dynamiques) |
  | Reporting automatisé | Générer des rapports avec métriques de réussite, défaillances et tendances prédictives |
  | Analyse des causes racines | Compiler des rapports de défauts complets avec logs, captures d'écran et données d'environnement |

**Défis spécifiques GUI vs API**
📊 Type | Défi | Solution GenAI
  | Tests GUI | Instabilité due aux changements UI récurrents | Adaptation automatique des localisateurs dynamiques et interactions modifiées |
  | Tests API | Modification des formats requête/réponse, endpoints, authentification | Adaptation automatique aux specs API évolutives + génération de données de test diversifiées |
📌 Rappel critique: L'IA générative peut faire des erreurs . La sortie générée doit être soigneusement vérifiée , en fonction du risque associé (cf. chapitre 3).

===========================================================================
SECTION: s224 — 2.2.4 Suivi et contrôle des tests
===========================================================================
🎯 GenAI-2.2.4 (K3) — Appliquer l'IA générative aux tâches de suivi et contrôle

**4 tâches de suivi et contrôle**
📊 Tâche | Description
  | Suivi et analyse des métriques | Automatiser le suivi de l'avancement, analyser les tendances, prévoir les risques, alerter en cas d'écart au plan |
  | Contrôle des activités | Fournir des informations pour reprioriser les tests, ajuster le calendrier et réaffecter les ressources |
  | Clôture et apprentissage | Générer des rapports de clôture mettant en évidence les réussites et les leçons apprises |
  | Visualisation et reporting | Créer des tableaux de bord dynamiques et des résumés en langage naturel pour toutes les parties prenantes |
📌 Point clé: Les données de suivi sont souvent non structurées et déjà disponibles dans les outils de gestion des tests. La GenAI excelle à les analyser et les synthétiser en informations exploitables.

===========================================================================
SECTION: s225 — 2.2.5 Choisir une technique de prompting
===========================================================================
🎯 GenAI-2.2.5 (K3) — Sélectionner les techniques de prompting appropriées
Ce tableau est critique pour l'examen — il faut savoir associer chaque technique à son cas d'utilisation :
📊 Technique | Cas d'utilisation | Caractéristiques
  | Enchaînement de prompts | Tâches complexes nécessitant une vérification humaine à chaque étape | Divise en sous-tâches, vérifie chaque étape. Utile pour analyse, conception, automatisation. |
  | Few-shot prompting | Tâches répétitives ou avec contraintes de format de sortie | Fournit des exemples pour guider. Gherkin, keyword-driven, reporting avec format spécifique. |
  | Méta-prompting | Tâches flexibles et dynamiques, création de prompts pour de nouvelles tâches | Le LLM crée/améliore le prompt. Analyse de rapports, détection d'anomalies. |
📌 Combinaison des techniques: Méta-prompting → crée un prompt initial Few-shot → on ajoute/adapte des exemples dans ce prompt Enchaînement → on divise en sous-tâches pour valider les étapes intermédiaires

===========================================================================
SECTION: s231 — 2.3.1 Métriques d'évaluation des résultats GenAI
===========================================================================
🎯 GenAI-2.3.1 (K2) — Comprendre les métriques d'évaluation des résultats GenAI
7 métriques pour évaluer la qualité des résultats du LLM sur une tâche de test :
📊 Métrique | Ce qu'elle mesure | Exemple
  | Exactitude | Fidélité globale vs référence experte ou prédéfinie | Degré de couverture des exigences par les cas générés |
  | Précision | Exactitude par rapport à un objectif spécifique | Les cas identifient-ils correctement les anomalies ? |
  | Rappel | Capacité à identifier TOUTES les instances pertinentes | Couverture des partitions d'équivalence valides et invalides |
  | Pertinence contextuelle | Adéquation au contexte donné | Cohérence avec la base de test et les exigences du domaine |
  | Diversité | Couverture d'un large éventail de scénarios | Comportements utilisateurs variés et cas aux limites |
  | Taux de réussite d'exécution | Proportion de scripts exécutables sans erreur | Combien de scripts s'exécutent sans erreurs de syntaxe |
  | Efficience temporelle | Temps gagné vs travail manuel | Temps GenAI pour générer les cas vs temps humain |
📌 Non-déterminisme: Vu la nature non déterministe de la GenAI, les métriques doivent être basées sur des données statistiquement pertinentes (plusieurs exécutions, pas une seule).

===========================================================================
SECTION: s232 — 2.3.2 Techniques d'affinage itératif
===========================================================================
🎯 GenAI-2.3.2 (K2) — Techniques d'évaluation et d'affinage itératif
5 techniques pour améliorer progressivement les résultats de la GenAI :
📊 Technique | Description
  | Modification itérative | Partir d'un prompt de base, le modifier progressivement en ajoutant du contexte ou en ajustant la formulation et la terminologie |
  | Tests A/B des prompts | Créer plusieurs versions du prompt et évaluer lequel produit les meilleurs résultats selon des métriques prédéfinies |
  | Analyse des résultats | Examiner les résultats pour détecter inexactitudes et incohérences (ex: vs la base de test). Comprendre les types d'erreurs pour les corriger |
  | Retours utilisateurs | Recueillir les commentaires des testeurs sur l'utilité et la clarté des résultats pour affiner les prompts |
  | Ajustement longueur/spécificité | Tester différentes longueurs. Plus de contexte peut améliorer la qualité, mais parfois des prompts plus courts donnent de meilleurs résultats |
📌 Culture d'équipe: Le syllabus insiste sur le partage des pratiques au sein de l'équipe : normaliser les techniques, partager des bibliothèques de prompts , éviter les erreurs répétées, et promouvoir une culture d'amélioration continue.
📌 Ce qu'on peut vous demander: Identifier quelle technique d'affinage correspond à quelle description. Exemple : « Créer plusieurs versions d'un prompt et comparer les résultats » → Tests A/B.

===========================================================================
FIN DU CHAPITRE 2
===========================================================================