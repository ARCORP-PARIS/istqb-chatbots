# istqb-chatbots

Assistants pédagogiques RAG pour les formations ISTQB de la plateforme certif-academy.

## Architecture

Monorepo conçu pour héberger **plusieurs chatbots** (un par certification) dans une seule
application FastAPI. Chaque chatbot dispose de son propre corpus de documents et de sa
propre collection ChromaDB, mais partage le même code applicatif.

```
istqb-chatbots/
├── app.py              ← Application Streamlit (dev/debug local — phase 1)
├── ingest.py           ← Pipeline d'ingestion (chunke + embeddings + Chroma)
├── corpus/             ← Documents bruts, organisés par certification
│   └── genai/
│       ├── cours/      ← Explications pédagogiques par chapitre
│       ├── faq/        ← Foire aux questions
│       ├── quiz/       ← Questions d'auto-évaluation
│       ├── revision/   ← Fiches de révision
│       └── syllabus/   ← Syllabus officiel ISTQB
├── chroma_db/          ← Vector store local (gitignored, régénéré via ingest.py)
├── venv/               ← Environnement Python (gitignored)
├── .env                ← Clés API (gitignored — voir .env.example)
└── requirements.txt
```

## Stack technique

- **Embeddings** : OpenAI `text-embedding-3-small`
- **LLM** : OpenAI `gpt-4.1-mini` (température 0.1)
- **Vector store** : ChromaDB (persistant local)
- **UI** : Streamlit (phase 1, dev/debug)

## Démarrage rapide

```bash
# 1. Installer
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configurer
cp .env.example .env
# → ouvre .env et colle ta vraie OPENAI_API_KEY

# 3. Ingérer le corpus
python ingest.py

# 4. Lancer
streamlit run app.py
```

## Stratégie de retrieve

Le système actuel privilégie la **section** comme unité de réponse :

1. Top 12 chunks récupérés par similarité d'embedding
2. Chunks regroupés par (chapitre, section)
3. La section avec le plus de chunks "matchés" devient le contexte principal

Cette approche évite le mélange de chapitres et garantit une réponse cohérente, ancrée
dans une seule partie du syllabus.

## Suite (phase 2)

- Portage Streamlit → FastAPI (endpoint REST `/chat`)
- Paramétrage par certification (collection + system prompt + filtres)
- Auth JWT Supabase (intégration certif-academy)
- Gate "5/5 chapitres terminés"
- Déploiement Fly.io
