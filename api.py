"""
FastAPI server pour le chatbot ISTQB GenAI.

Phase 3 — port + auth JWT Supabase + déploiement Fly.io.

Lancement local :
    uvicorn api:app --reload --port 8000

Endpoints :
    GET  /health  -> {"status": "ok", ...}   (PUBLIC, pas d'auth)
    POST /chat    -> {"answer": "...", ...}  (AUTH REQUIRED : JWT Supabase)

Auth :
    Le client (frontend certif-academy) doit envoyer un header
    `Authorization: Bearer <supabase-access-token>`. La validation est
    déléguée à Supabase en appelant `GET {SUPABASE_URL}/auth/v1/user`
    avec le token. C'est un appel HTTP supplémentaire par requête /chat,
    mais ça évite d'avoir besoin du JWT Secret (que Lovable Cloud ne nous
    expose pas). Le `user.id` renvoyé est récupéré pour usage futur
    (gate "5/5 chapitres", métriques).

NB : la base Chroma (./chroma_db en dev, /data/chroma_db sur Fly via
volume monté) est générée par `python ingest.py`. Aucun appel réseau
hors OpenAI à l'exécution.
"""

import os
from typing import Annotated, List, Optional

import chromadb
import httpx
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY manquant. Crée un fichier .env (cf .env.example)."
    )

SUPABASE_URL = os.getenv("SUPABASE_URL")
if not SUPABASE_URL:
    raise RuntimeError(
        "SUPABASE_URL manquant. Format attendu : https://<ref>.supabase.co."
        " Récupérable côté Lovable (var d'env du projet) ou sur Supabase."
    )
SUPABASE_URL = SUPABASE_URL.rstrip("/")

SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
if not SUPABASE_ANON_KEY:
    raise RuntimeError(
        "SUPABASE_ANON_KEY manquant. C'est la \"publishable key\" du projet"
        " Supabase (clé publique, exposable au navigateur)."
    )

# URL absolue de l'endpoint qui sert à valider un access_token utilisateur.
# Supabase répond 200 + JSON {id, email, ...} si le token est valide,
# 401 sinon. Référence : https://supabase.com/docs/reference/api/auth
SUPABASE_USER_ENDPOINT = f"{SUPABASE_URL}/auth/v1/user"

CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "istqb_knowledge")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4.1-mini")
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")

# Liste blanche d'origines : dev local (Vite) + prod Lovable.
# Surchargeable via env var ALLOWED_ORIGINS (CSV).
DEFAULT_ORIGINS = ",".join(
    [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "https://skill-architect-core.lovable.app",
    ]
)
ALLOWED_ORIGINS = [
    o.strip()
    for o in os.getenv("ALLOWED_ORIGINS", DEFAULT_ORIGINS).split(",")
    if o.strip()
]

# ---------------------------------------------------------------------------
# Clients (chargés une fois au démarrage)
# ---------------------------------------------------------------------------

openai_client = OpenAI(api_key=OPENAI_API_KEY)
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_collection(name=COLLECTION_NAME)

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="ISTQB GenAI chatbot API",
    version="0.2.0",
    description="Assistant de révision basé sur le syllabus officiel ISTQB GenAI.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------


class Message(BaseModel):
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str = Field(..., min_length=1, max_length=4000)


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    history: List[Message] = Field(default_factory=list)


class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
    chapter_hint: Optional[str] = None


# ---------------------------------------------------------------------------
# Auth : JWT Supabase
# ---------------------------------------------------------------------------


def get_current_user(
    authorization: Annotated[Optional[str], Header()] = None,
) -> str:
    """Valide le JWT Supabase en déléguant à Supabase.

    Le frontend (certif-academy) doit envoyer :
        Authorization: Bearer <supabase-access-token>

    On délègue la validation à Supabase via `GET /auth/v1/user` : si la
    réponse est 200, le token est bon et on récupère le `id` utilisateur.
    Sinon → 401. C'est un appel HTTP par requête /chat (Supabase est
    rapide, ~100ms ; on optimisera plus tard avec un cache court si
    nécessaire).

    Pourquoi pas de validation locale HS256 ? Parce que Lovable Cloud
    gère le projet Supabase et n'expose pas le JWT Secret aux clients.
    """
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or malformed Authorization header.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.split(" ", 1)[1].strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Empty bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        resp = httpx.get(
            SUPABASE_USER_ENDPOINT,
            headers={
                "apikey": SUPABASE_ANON_KEY,
                "Authorization": f"Bearer {token}",
            },
            timeout=5.0,
        )
    except httpx.HTTPError as exc:
        # Supabase joignable mais lent / TLS / DNS… on remonte un 503 pour
        # que le frontend ne traite pas ça comme une erreur d'auth.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Auth provider unreachable: {exc}",
        )

    if resp.status_code != 200:
        # Vague volontaire — pas la peine de dire à un attaquant si c'est
        # le token qui est expiré ou mal formé.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = resp.json()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Auth provider returned non-JSON response.",
        )

    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token user lookup returned no id.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id


# ---------------------------------------------------------------------------
# Logique RAG (portée depuis app.py)
# ---------------------------------------------------------------------------

IMPLICIT_FOLLOW_UP_KEYWORDS = [
    "ce que tu viens",
    "ce que tu as dit",
    "la réponse",
    "donne la réponse",
    "explique plus",
    "résume",
    "pourquoi",
    "donne un exemple",
    "pose moi une question",
    "sur ça",
    "sur ce sujet",
    "dessus",
    "ça",
]


def is_implicit_follow_up(question: str) -> bool:
    q = question.lower()
    return any(k in q for k in IMPLICIT_FOLLOW_UP_KEYWORDS)


def build_search_query(question: str, history: List[Message]) -> str:
    """Memory lock : si la question est implicite, on enrichit le query
    de recherche avec le dernier message assistant."""
    if not is_implicit_follow_up(question):
        return question
    last_assistant = next(
        (m.content for m in reversed(history) if m.role == "assistant"),
        "",
    )
    if not last_assistant:
        return question
    return f"{last_assistant}\n\nInstruction utilisateur : {question}"


def retrieve_best_section(query: str):
    """V6 MONO SECTION : top 12 chunks → groupés par (chapitre, section)
    → on garde la section la plus matchée pour éviter le mélange de chapitres."""
    q_emb = openai_client.embeddings.create(
        model=EMBED_MODEL,
        input=query,
    ).data[0].embedding

    results = collection.query(
        query_embeddings=[q_emb],
        n_results=12,
        where={"category": "syllabus"},
    )

    docs = results["documents"][0] if results["documents"] else []
    metas = results["metadatas"][0] if results["metadatas"] else []

    if not docs:
        return [], [], None

    section_groups: dict = {}
    for doc, meta in zip(docs, metas):
        key = (meta.get("chapter", "NA"), meta.get("section", "NA"))
        if key not in section_groups:
            section_groups[key] = {"docs": [], "meta": meta}
        section_groups[key]["docs"].append(doc)

    best = max(section_groups.values(), key=lambda x: len(x["docs"]))
    return best["docs"], metas, best["meta"]


# Prompt repris quasi-mot pour mot depuis app.py (juste isolé en constante).
SYSTEM_PROMPT_TEMPLATE = """
Tu es un assistant pédagogique spécialisé exclusivement dans la formation ISTQB GenAI.

MISSION :
Aider l'élève à comprendre, réviser et maîtriser les notions ISTQB GenAI uniquement à partir du syllabus.

SOURCE UNIQUE :
- Utilise uniquement le syllabus fourni.
- Ignore totalement Internet et connaissances externes.

PÉRIMÈTRE :
- Réponds uniquement aux questions ISTQB GenAI.
- Utilise l'historique si la question est implicite.

FIABILITÉ :
- N'invente jamais.
- Si absent du syllabus :
"Je n'ai pas trouvé cette information dans la formation."

MÉMOIRE :
- Utilise l'historique pour comprendre :
ça, explique plus, résume, donne la réponse.

SYLLABUS :
- Priorise une seule section si possible.
- Évite le mélange de chapitres.

FORMAT DE RÉPONSE :

Pour une définition :

Définition :
...

📍 À réviser : ...

Pour une explication :

Points clés :
- ...
- ...
- ...

📍 À réviser : ...

Pour une comparaison :

Comparaison :
- ...
- ...

📍 À réviser : ...

STYLE :
- Réponds en français.
- Sois clair, fiable et précis.
- Réponse courte par défaut.
- Va directement à l'essentiel.
- Évite les longues introductions.
- Évite les répétitions.
- Évite les formulations génériques de type assistant IA.
- Utilise uniquement les informations utiles à la compréhension de la notion.
- Favorise les définitions ISTQB.
- Favorise les réponses adaptées à la préparation d'un examen.
- Si la question demande une définition, commence directement par la définition.
- Si la question demande une explication, structure la réponse en points clés.
- Ne rédige jamais de longs paragraphes si une réponse courte suffit.

RÉVISION :
- Termine systématiquement chaque réponse par :

📍 À réviser : Chapitre X — Section Y

- Si la section exacte n'est pas connue :

📍 À réviser : Chapitre concerné

- La mention de révision est obligatoire.

Historique :
{conversation_history}

Contexte :
{context}

Question :
{question}
"""


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": CHAT_MODEL,
        "collection": COLLECTION_NAME,
    }


@app.post("/chat", response_model=ChatResponse)
def chat(
    req: ChatRequest,
    user_id: Annotated[str, Depends(get_current_user)],
):
    # `user_id` est le `sub` du JWT Supabase. On le récupère pour pouvoir
    # logger / appliquer plus tard la gate "5/5 chapitres terminés".
    _ = user_id

    # Mémoire : on garde les 10 derniers messages (5 échanges).
    history = req.history[-10:]

    search_query = build_search_query(req.question, history)

    docs, all_metas, primary_meta = retrieve_best_section(search_query)

    if not docs:
        return ChatResponse(
            answer="Je n'ai pas trouvé cette information dans la formation.",
            sources=[],
            chapter_hint=None,
        )

    context = "\n\n---\n\n".join(docs)
    sources = sorted(
        {f"{m.get('category')} / {m.get('source')}" for m in all_metas}
    )

    conversation_history = "\n".join(
        f"{m.role}: {m.content}" for m in history
    )

    prompt = SYSTEM_PROMPT_TEMPLATE.format(
        conversation_history=conversation_history,
        context=context,
        question=req.question,
    )

    try:
        completion = openai_client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
    except Exception as e:
        # On ne renvoie pas le message d'erreur OpenAI brut au client.
        raise HTTPException(
            status_code=502,
            detail=f"OpenAI upstream error ({type(e).__name__})",
        )

    answer = (completion.choices[0].message.content or "").strip()
    chapter_hint = primary_meta.get("chapter") if primary_meta else None

    return ChatResponse(
        answer=answer,
        sources=sources,
        chapter_hint=chapter_hint,
    )
