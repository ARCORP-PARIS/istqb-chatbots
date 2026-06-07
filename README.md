# istqb-chatbots

Assistants pédagogiques RAG pour les formations ISTQB de la plateforme certif-academy.

## Architecture

Monorepo conçu pour héberger **plusieurs chatbots** (un par certification) dans une seule
application FastAPI. Chaque chatbot dispose de son propre corpus de documents et de sa
propre collection ChromaDB, mais partage le même code applicatif.

```
istqb-chatbots/
├── api.py              ← Application FastAPI (phase 2 — consommée par le frontend)
├── app.py              ← Ancienne UI Streamlit (conservée pour debug local)
├── ingest.py           ← Pipeline d'ingestion (chunke + embeddings + Chroma)
├── corpus/             ← Documents bruts, organisés par certification
│   └── genai/
│       └── syllabus/   ← Syllabus officiel ISTQB GenAI (seul ingéré)
├── chroma_db/          ← Vector store local (gitignored, régénéré via ingest.py)
├── venv/               ← Environnement Python (gitignored)
├── .env                ← Clés API (gitignored — voir .env.example)
└── requirements.txt
```

> **Note** : les sous-dossiers `cours/`, `faq/`, `quiz/`, `revision/` du corpus existent
> mais ne sont **pas** ingérés. Le site certif-academy a déjà ces contenus en interne ;
> le chatbot ne sert qu'à la révision basée sur la source officielle (syllabus).

## Stack technique

- **Embeddings** : OpenAI `text-embedding-3-small`
- **LLM** : OpenAI `gpt-4.1-mini` (température 0.1)
- **Vector store** : ChromaDB (persistant local)
- **API** : FastAPI + Uvicorn (phase 2)
- **UI legacy** : Streamlit (phase 1, conservée pour debug)

## Démarrage rapide

```bash
# 1. Installer
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configurer
cp .env.example .env
# → ouvre .env et colle ta vraie OPENAI_API_KEY

# 3. Ingérer le corpus (à refaire après tout changement dans corpus/)
python ingest.py

# 4a. Lancer en mode API (consommée par le frontend certif-academy)
uvicorn api:app --reload --port 8000

# 4b. (ou) lancer l'ancienne UI Streamlit pour tester en local
streamlit run app.py
```

## Endpoints API

### `GET /health`

Sonde de vie. Retourne `{"status": "ok", "model": "...", "collection": "..."}`.

### `POST /chat`

Pose une question au chatbot.

**Body :**
```json
{
  "question": "Qu'est-ce qu'un prompt injection ?",
  "history": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

**Réponse :**
```json
{
  "answer": "Définition :\n...\n\n📍 À réviser : Chapitre 4 — Section 4.2",
  "sources": ["syllabus / chapitre_4_syllabus.md"],
  "chapter_hint": "Chapitre 4"
}
```

L'historique est facultatif. Côté frontend, on envoie idéalement les 10 derniers
messages (5 échanges) pour assurer la mémoire conversationnelle.

### Test rapide

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Définis prompt injection.", "history": []}'
```

## Stratégie de retrieve

Le système privilégie la **section** comme unité de réponse :

1. Top 12 chunks récupérés par similarité d'embedding (filtre `category=syllabus`)
2. Chunks regroupés par (chapitre, section)
3. La section avec le plus de chunks "matchés" devient le contexte principal

Cette approche évite le mélange de chapitres et garantit une réponse cohérente, ancrée
dans une seule partie du syllabus.

## CORS

`api.py` autorise par défaut `http://localhost:5173` (Vite), `http://localhost:3000`
et `http://127.0.0.1:5173`. Pour ajuster, définir `ALLOWED_ORIGINS` dans `.env` :

```
ALLOWED_ORIGINS=http://localhost:5173,https://certif-academy.example.com
```

## Suite (phase 3)

- Auth JWT Supabase (intégration certif-academy)
- Gate "5/5 chapitres terminés" côté API
- Déploiement Fly.io (volume monté pour persister `chroma_db/`)
- Ajout du second chatbot ISTQB Foundation (`corpus/foundation/syllabus/`)
