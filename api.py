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
    `Authorization: Bearer <supabase-access-token>`. Les tokens Supabase
    sont signés en ES256 (asymétrique, courbe P-256). On valide la
    signature en local avec la clé publique servie par
    `{SUPABASE_URL}/auth/v1/.well-known/jwks.json`. La clé est cachée par
    `PyJWKClient` (TTL 1h), donc aucun appel réseau dans le chemin chaud
    d'une requête /chat. On récupère le `sub` (user id) pour usage futur
    (gate "5/5 chapitres", métriques).

NB : la base Chroma (./chroma_db en dev, /data/chroma_db sur Fly via
volume monté) est générée par `python ingest.py`. Aucun appel réseau
hors OpenAI à l'exécution.
"""

import os
from typing import Annotated, List, Optional

import chromadb
import jwt
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from jwt import PyJWKClient, PyJWKClientError
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

# URL du JWKS Supabase. Sert à récupérer la clé publique ES256 qui valide
# les tokens utilisateur. Surchargeable au cas où Supabase change le path.
SUPABASE_JWKS_URL = os.getenv(
    "SUPABASE_JWKS_URL",
    f"{SUPABASE_URL}/auth/v1/.well-known/jwks.json",
)

# Audience attendue dans le JWT. Pour les sessions utilisateur Supabase
# classiques, c'est "authenticated". Mettre à vide pour désactiver le
# check d'audience (utile si Supabase change la convention).
SUPABASE_JWT_AUDIENCE = os.getenv("SUPABASE_JWT_AUDIENCE", "authenticated")

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
# get_or_create_collection : permet à l'app de booter même si le volume
# Fly est encore vide (cas du tout 1er déploiement, avant ingest.py).
# Sans ça, get_collection() lèverait NotFoundError et l'app crashait
# au démarrage → healthcheck KO → deploy timeout.
collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

# JWKS Supabase : récupère et cache la clé publique ES256. La 1re requête
# /chat après le démarrage fait un appel réseau pour fetch les keys, puis
# le client les garde en mémoire pendant `lifespan` secondes (1h par défaut
# côté PyJWT).
jwks_client = PyJWKClient(SUPABASE_JWKS_URL, cache_keys=True, lifespan=3600)

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
    """Valide localement le JWT Supabase (ES256, clé publique JWKS).

    Le frontend (certif-academy) envoie :
        Authorization: Bearer <supabase-access-token>

    Les tokens Supabase sont signés en ES256 (asymétrique). On récupère
    la clé publique correspondante via le JWKS (cachée par `jwks_client`
    pendant 1h) et on vérifie la signature + l'expiration en local. Pas
    d'appel réseau par requête /chat.

    Retourne le `sub` du JWT = user.id Supabase.
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

    # 1) Récupère la clé publique qui correspond au `kid` du token.
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
    except PyJWKClientError as exc:
        # Le JWKS est injoignable / le kid n'est pas trouvé. On distingue
        # via le 503 pour que le frontend ne marque pas l'utilisateur
        # comme non-authentifié à tort.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"JWKS unavailable: {exc}",
        )

    # 2) Vérifie la signature, l'expiration et (si activé) l'audience.
    decode_kwargs = {
        "algorithms": ["ES256"],
        "options": {"require": ["exp", "sub"]},
    }
    if SUPABASE_JWT_AUDIENCE:
        decode_kwargs["audience"] = SUPABASE_JWT_AUDIENCE

    try:
        payload = jwt.decode(token, signing_key.key, **decode_kwargs)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        # On reste volontairement vague (mauvais aud, mauvaise signature,
        # `sub` manquant…) pour ne pas guider un attaquant.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        # Filet de sécurité : `require: ["sub"]` doit déjà l'avoir attrapé.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing subject.",
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
    """V7 TOP-2 SECTIONS : top 20 chunks → groupés par (chapitre, section)
    → on concatène les 2 sections les plus matchées dans le contexte. Ça
    couvre les questions transverses (ex: "types de LLM" touche 1.1.3 ET
    1.1.4) sans réintroduire le mélange chaotique d'origine. `primary_meta`
    = section dominante (sert au hint chapitre côté UI)."""
    q_emb = openai_client.embeddings.create(
        model=EMBED_MODEL,
        input=query,
    ).data[0].embedding

    results = collection.query(
        query_embeddings=[q_emb],
        n_results=20,
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

    top_sections = sorted(
        section_groups.values(),
        key=lambda x: len(x["docs"]),
        reverse=True,
    )[:2]

    combined_docs: list = []
    for s in top_sections:
        combined_docs.extend(s["docs"])

    primary_meta = top_sections[0]["meta"] if top_sections else None
    return combined_docs, metas, primary_meta


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
- N'invente jamais d'informations qui contredisent le contexte fourni.
- Si la question porte sur une notion adjacente présente dans le contexte (même partiellement), réponds avec ce que tu trouves en commençant par : "Le syllabus n'aborde pas directement ce point, mais voici les éléments liés :".
- Ne réponds "Je n'ai pas trouvé cette information dans la formation." QUE si le contexte fourni n'a vraiment AUCUN rapport avec la question.

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
