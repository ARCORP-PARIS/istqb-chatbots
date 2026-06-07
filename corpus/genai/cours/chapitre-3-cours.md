===========================================================================
CHAPITRE 3 — GÉRER LES RISQUES DE LA GENAI
===========================================================================
Le chapitre 3 couvre tous les risques liés à l'utilisation de la GenAI dans les tests : hallucinations, biais, confidentialité, sécurité, impact environnemental et réglementations.

===========================================================================
SECTION: s311 — 3.1.1 Hallucinations, erreurs de raisonnement, biais
===========================================================================
🎯 GenAI-3.1.1 (K1) — Rappeler les définitions des hallucinations, erreurs et biais
Les LLMs sont sujets à **3 types de défauts** qui réduisent la qualité de leurs résultats :
📊 Défaut | Définition | Exemples en test logiciel
  | Hallucination | Le LLM génère une sortie factuellement incorrecte ou non pertinente pour la tâche | Cas de test fictifs, scripts incorrects, critères d'acceptation inexistants dans la User Story |
  | Erreur de raisonnement | Le LLM interprète mal les structures logiques (cause-effet, logique conditionnelle, résolution multi-étapes) → conclusions incorrectes | Mauvaise priorisation des cas de test, estimation d'effort incohérente, erreurs dans le raisonnement mathématique |
  | Biais | Le LLM produit des résultats qui favorisent certains types d'informations à cause des données d'entraînement | Sous-représentation des tests non fonctionnels, données de test non diversifiées, biais linguistique (anglophone) |
📌 Cause fondamentale: Ces 3 défauts résultent de la **nature des données d'entraînement** et des 
 **limites du modèle Transformer**. Les LLMs ne disposent pas d'un véritable
 raisonnement logique — ils s'appuient sur la **reconnaissance de motifs**.
📌 Mots-clés à retenir: Mots-clés: hallucination, erreur de raisonnement, biais, température

===========================================================================
SECTION: s312 — 3.1.2 Identifier les problèmes
===========================================================================
🎯 GenAI-3.1.2 (K3) — Analyser les hallucinations, erreurs et biais dans les résultats
Différentes approches de détection selon le type de problème. La détection combine revue humaine et vérification automatisée.

**Détecter les hallucinations**
📊 Méthode | Description
  | Vérification croisée | Comparer les résultats avec la documentation existante, les exigences et le comportement connu du système. Des outils automatisés peuvent recouper avec des sources établies. |
  | Consultation d'experts | Faire appel à des experts du domaine pour valider l'exactitude. Ils captent les nuances que l'automatisation manque. |
  | Contrôles de cohérence | Vérifier que les résultats sont cohérents entre eux et avec les informations connues. Automatisable pour détecter les patterns d'erreurs. |

**Détecter les erreurs de raisonnement**
📊 Méthode | Description
  | Validation logique | Évaluer le flux logique (cohérence, raisonnement structuré) via des cycles de revue. Les cas complexes nécessitent un jugement humain. |
  | Test des résultats | Exécuter les cas/scripts de test générés sur les objets de test pour vérifier. Partiellement ou totalement automatisable. |

**Détecter les biais**
📊 Méthode | Description
  | Revue de représentation | Vérifier que les testware générés (données synthétiques) sont représentés de manière équitable par rapport à la stratégie de test. |
  | Évaluation par type de test | Vérifier s'il y a sous-représentation de certains types de tests (ex: tests non fonctionnels) dans les résultats. |
📌 Exercices pratiques: **HO-3.1.2a (H1)** — Confronter au moins 2 LLMs à une situation générant des
 hallucinations. Tester différents prompts pour observer leur influence.
 **HO-3.1.2b (H1)** — Tester un problème de planification/estimation avec 3 types de
 LLM (LLM, SLM, modèle de raisonnement) et comparer au résultat exact.

===========================================================================
SECTION: s313 — 3.1.3 Techniques d'atténuation
===========================================================================
🎯 GenAI-3.1.3 (K2) — Résumer les techniques d'atténuation
Ces problèmes surviennent surtout quand les **prompts sont mal conçus** ou quand les **données contextuelles manquent**. Voici les 5 techniques clés d'atténuation :
📊 Technique | Description
  | Contexte complet | Le prompt doit contenir toutes les informations pertinentes (structure en 6 composants, cf. chapitre 2) |
  | Diviser en sous-tâches | Enchaînement de prompts : vérifier chaque sortie avant de passer à la suivante. Détecte les erreurs de raisonnement tôt. |
  | Formats clairs | Utiliser des formats structurés et simples, éviter l'ambiguïté dans les données d'entrée |
  | Choisir le bon modèle | Utiliser un LLM adapté à la tâche (cf. section 5.1.3). Modèle de raisonnement pour les tâches complexes. |
  | Comparer entre modèles | Évaluer le prompt avec plusieurs LLMs et comparer les résultats pour détecter les erreurs |
📌 Techniques complémentaires (chapitre 4): Deux techniques avancées améliorent aussi les résultats : le **RAG** 
 (Retrieval-Augmented Generation) et le **Fine-Tuning**. Elles seront couvertes au
 chapitre 4.

===========================================================================
SECTION: s314 — 3.1.4 Non-déterminisme
===========================================================================
🎯 GenAI-3.1.4 (K1) — Rappeler les techniques d'atténuation du non-déterminisme
Le non-déterminisme = la même entrée peut produire des résultats différents. Il résulte des **processus d'échantillonnage probabilistes** lors de l'inférence. Particulièrement problématique pour les résultats longs.

**2 stratégies pour réduire la variabilité**
📊 Stratégie | Comment ça marche | Limite
  | Ajuster la température | Abaisser la température réduit la distribution de probabilité → résultats plus cohérents et moins aléatoires | Limite la créativité et la diversité, résultats plus répétitifs |
  | Définir des graines aléatoires (random seeds) | Fixer une valeur de seed pour le générateur aléatoire → même séquence pseudo-aléatoire → meilleure reproductibilité | Pas disponible sur toutes les implémentations |
📌 Point examen: La reproductibilité totale est **impossible à garantir**. On peut seulement 
 **réduire** la variabilité. L'automatisation de la vérification des résultats aide à
 mettre en place un processus d'évaluation structuré et cohérent.

===========================================================================
SECTION: s321 — 3.2.1 Risques de confidentialité et sécurité
===========================================================================
🎯 GenAI-3.2.1 (K2) — Expliquer les risques de confidentialité et sécurité

**Risques de confidentialité des données**
📊 Risque | Description
  | Exposition involontaire | Le LLM peut générer des résultats qui révèlent accidentellement des informations sensibles |
  | Manque de contrôle sur les données | Les outils GenAI peuvent stocker/traiter des données sensibles sans consentement explicite → utilisation abusive ou accès non autorisé |
  | Non-conformité réglementaire | Utilisation sans respecter le RGPD → risque de litiges juridiques |

**Risques de sécurité spécifiques**
  • Les **infrastructures de test basées sur LLM** sont vulnérables aux violations de données et accès non autorisés
  • Les **acteurs malveillants** peuvent exploiter les vulnérabilités (attaques manipulatrices) pour modifier le comportement du LLM ou extraire des infos sensibles
  • Les **données d'entrée malveillantes** peuvent tromper les LLMs et compromettre leur précision ou sécurité
📌 Mots-clés à retenir: Mots-clés: confidentialité des données, sécurité, vulnérabilité, RGPD

===========================================================================
SECTION: s322 — 3.2.2 Vecteurs d'attaque
===========================================================================
🎯 GenAI-3.2.2 (K2) — Exemples de vulnérabilités et vecteurs d'attaque
📊 Vecteur | Description | Exemple concret
  | Exfiltration de données | Prompts conçus pour extraire des données confidentielles d'entraînement | Dépasser la fenêtre contextuelle avec de longs prompts pour surcharger la mémoire → le LLM révèle des extraits de ses données d'entraînement |
  | Manipulation des prompts | Introduction de données qui perturbent les résultats | Images qui induisent le LLM dans un contexte différent, provoquant des hallucinations sur les critères d'acceptation |
  | Contamination des données | Manipulation des données d'entraînement | Fournir de fausses évaluations lors de la notation des résultats d'un rapport de test généré par l'IA |
  | Génération de code malveillant | Manipuler un LLM pour générer des portes dérobées | Génération de code ouvrant un canal de communication vers une adresse IP malveillante |
📌 Risque critique: La **génération de code malveillant** est particulièrement dangereuse dans un
 contexte d'automatisation des tests — les scripts générés pourraient contenir des portes
 dérobées exécutées dans les environnements CI/CD.

===========================================================================
SECTION: s323 — 3.2.3 Stratégies d'atténuation sécurité
===========================================================================
🎯 GenAI-3.2.3 (K2) — Stratégies d'atténuation pour la sécurité

**Mesures de confidentialité des données**
📊 Mesure | Description
  | Minimisation des données | N'utiliser que la quantité nécessaire de données non sensibles. Éviter le traitement des données sensibles sauf obligation légale. |
  | Anonymisation / pseudonymisation | Masquer ou remplacer les informations sensibles par des données non identifiables |
  | Stockage et transmission sécurisés | Chiffrement puissant et contrôles d'accès stricts |
  | Formation du personnel | Programmes et politiques clairs pour une utilisation responsable des outils GenAI |

**Stratégies d'atténuation supplémentaires**
📊 Stratégie | Description
  | Revue systématique | Évaluation humaine obligatoire des résultats générés par le LLM |
  | Comparaison multi-LLM | Utiliser plusieurs LLMs sur une même tâche et comparer les réponses |
  | Environnement sécurisé | Selon la confidentialité : offre commerciale sécurisée, cloud sécurisé, ou LLM installé on-premise (dans l'infrastructure de l'organisation) |
  | Audits réguliers | Évaluations de vulnérabilités et correction proactive des faiblesses identifiées |
  | Veille sécuritaire | Se tenir informé des dernières directives, menaces et technologies de sécurité |
📌 Recommandation forte: Le syllabus recommande d'impliquer des **ingénieurs sécurité**, 
 **conseillers juridiques**, le **CTO** ou le **CISO** dans la mise en œuvre de
 ces stratégies.

===========================================================================
SECTION: s331 — 3.3.1 Impact environnemental
===========================================================================
🎯 GenAI-3.3.1 (K2) — Expliquer l'impact sur la consommation énergétique
L'entraînement et l'utilisation des LLMs nécessitent des **ressources informatiques intensives** → consommation d'énergie élevée → émissions de CO₂ significatives.

**Ordres de grandeur**
📊 Tâche GenAI | Consommation relative
  | Génération d'une image | Équivalent à la recharge complète d'un smartphone |
  | Génération de texte | Seulement un faible pourcentage de la charge d'un smartphone |
Une seule requête semble négligeable, mais l'**effet cumulé** sur des millions d'utilisateurs représente une pression environnementale considérable.
📌 Bonne pratique: Limiter les interactions inutiles avec les modèles. La complexité de la tâche et les
 ressources informatiques nécessaires influencent directement la consommation.
📌 Exercice pratique HO-3.3.1 (H1): Utiliser un simulateur pour calculer l'énergie et les émissions de CO₂ pour différentes
 tâches de test GenAI. Observer comment les caractéristiques des tâches et le choix du
 modèle affectent l'impact.

===========================================================================
SECTION: s341 — 3.4.1 Réglementations et normes
===========================================================================
🎯 GenAI-3.4.1 (K1) — Rappeler les réglementations, normes et cadres
4 références clés à connaître pour l'examen :
📊 Nom | Type | Description | Application test
  | ISO/IEC 42001:2023 | Norme | Exigences pour la gestion des systèmes d'IA au sein d'une organisation | Cohérence et fiabilité de la GenAI dans les tests |
  | ISO/IEC 23053:2022 | Norme | Cadre pour les systèmes d'IA utilisant le ML — sûreté et transparence | Qualité des données, transparence, sûreté dans les tests GenAI |
  | EU AI Act | Réglementation | Cadre juridique classant les applications IA par niveau de risque | Conformité en transparence, responsabilité et atténuation des biais |
  | NIST AI RMF (US) | Framework | Recommandations de gestion des risques IA — équité, transparence, sécurité | Garantir l'équité, éviter les résultats de test biaisés |
📌 Astuce examen: Retiens le type de chaque référence : **ISO = normes**, 
 **EU AI Act = réglementation** (loi), **NIST = framework** (recommandations). Les
 questions peuvent demander de classer un élément dans la bonne catégorie.
📌 Évolution continue: Le syllabus insiste : les technologies IA et leur cadre réglementaire 
 **continuent d'évoluer**. Les organismes de test doivent se tenir informés en
 permanence.