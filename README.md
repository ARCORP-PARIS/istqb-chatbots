# istqb-chatbots

Assistants pédagogiques RAG pour les formations ISTQB de la plateforme certif-academy.

## Architecture

Monorepo conçu pour héberger **plusieurs chatbots** (un par certification) dans une seule
application FastAPI. Chaque chatbot dispose de son propre corpus de documents et de sa
propre collection ChromaDB, mais partage le même code applicatif.

```
istqb-chatbots/
├── api.py              ← Application FastAPI (phase 3 — auth JWT + déploiement Fly)
├── app.py              ← Ancienne UI Streamlit (conservée pour debug local)
├── ingest.py           ← Pipeline d'ingestion (chunke + embeddings + Chroma)
├── corpus/             ← Documents bruts, organisés par certification
│   └── genai/
│       └── syllabus/   ← Syllabus officiel ISTQB GenAI (seul ingéré)
├── chroma_db/          ← Vector store local (gitignored, régénéré via ingest.py)
├── venv/               ← Environnement Python (gitignored)
├── .env                ← Clés API (gitignored — voir .env.example)
├── Dockerfile          ← Image prod (Python 3.11-slim + uvicorn)
├── .dockerignore       ← Exclusions build (venv, .env, chroma_db local, …)
├── fly.toml            ← Config Fly.io (région cdg, volume /data, /health)
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

## Auth (phase 3)

Le `POST /chat` exige un JWT Supabase. Le frontend doit envoyer :

```
Authorization: Bearer <supabase-access-token>
```

Les tokens Supabase sont signés en **ES256** (asymétrique, courbe P-256).
Le backend récupère la clé publique correspondante via le JWKS du projet :

```
{SUPABASE_URL}/auth/v1/.well-known/jwks.json
```

`PyJWKClient` fetch et cache le JWKS pendant 1h, donc la validation se
fait 100% en local après le 1er appel — aucun appel réseau dans le
chemin chaud d'une requête /chat. Pas besoin du JWT Secret (Lovable
Cloud ne l'expose pas).

Variable d'env requise côté backend :

```
SUPABASE_URL=https://<project-ref>.supabase.co
```

Optionnel : `SUPABASE_JWT_AUDIENCE` (défaut `authenticated`),
`SUPABASE_JWKS_URL` (override si Supabase change le path).

`GET /health` reste public (sonde Fly.io).

## Déploiement Fly.io

L'app tourne sur Fly.io en région `cdg` (Paris) avec un volume monté sur
`/data` pour persister `chroma_db/` entre les redémarrages.

```bash
# 0. Installer flyctl (une fois pour toutes)
curl -L https://fly.io/install.sh | sh

# 1. Login + créer l'app (sans déployer tout de suite)
fly auth login
fly launch --no-deploy --copy-config --name istqb-chatbots --region cdg

# 2. Créer le volume qui hébergera /data/chroma_db
fly volumes create chroma_data --region cdg --size 1

# 3. Pousser les secrets (OpenAI + Supabase URL)
fly secrets set \
  OPENAI_API_KEY=sk-... \
  SUPABASE_URL=https://<project-ref>.supabase.co

# 4. Premier déploiement
fly deploy

# 5. Ingestion initiale (le volume est vide au premier boot)
fly ssh console -C "python ingest.py"

# 6. Vérifier
curl https://istqb-chatbots.fly.dev/health
```

À chaque modification du corpus (`corpus/genai/syllabus/*.md`) :

```bash
fly deploy
fly ssh console -C "python ingest.py"
```

## Suite

- Gate "5/5 chapitres terminés" côté API (RPC Supabase appelée depuis
  `get_current_user` ou un middleware dédié)
- Ajout du second chatbot ISTQB Foundation (`corpus/foundation/syllabus/`)
- Métriques d'usage par `user_id` (pour suivre l'utilisation)
