# ---------------------------------------------------------------------------
# istqb-chatbots — image FastAPI pour Fly.io
# ---------------------------------------------------------------------------
# Build :     fly deploy   (depuis ce dossier, avec fly.toml à la racine)
# Run local : docker build -t istqb-chatbots . && docker run -p 8000:8000 \
#               -e OPENAI_API_KEY=... -e SUPABASE_JWT_SECRET=... istqb-chatbots
# ---------------------------------------------------------------------------

FROM python:3.11-slim AS base

# Empêche Python de bufferiser stdout (logs en temps réel sur Fly).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Dépendances système minimales (chromadb tire sqlite + sentence-transformers
# en option ; on installe juste ce qu'il faut pour pip + healthchecks).
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && rm -rf /var/lib/apt/lists/*

# --- Dépendances Python -----------------------------------------------------
# On copie d'abord requirements.txt seul pour profiter du cache Docker tant
# que les deps ne changent pas.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Code applicatif --------------------------------------------------------
COPY api.py ingest.py ./
COPY corpus/ ./corpus/

# Le volume Fly sera monté ici (cf fly.toml [mounts]). Si tu lances `ingest.py`
# en one-shot via `fly ssh console`, il écrira directement dans /data/chroma_db.
ENV CHROMA_PATH=/data/chroma_db

EXPOSE 8000

# Uvicorn en prod : pas de --reload, on respecte le PORT injecté par Fly
# (par défaut 8000, mappé sur 80/443 par fly.toml).
CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}"]
