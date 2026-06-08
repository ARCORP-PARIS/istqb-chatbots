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
import time
from typing import Annotated, List, Optional

import chromadb
import httpx
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

# Phase 4 — Gate "5/5 chapitres terminés OU admin override".
# On appelle une RPC Supabase `is_chatbot_unlocked()` qui retourne TRUE/FALSE
# pour l'utilisateur courant. La RPC est SECURITY DEFINER côté Supabase et
# utilise auth.uid() en interne, donc impossible de chercher l'unlock status
# d'un autre user.
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
# Bypass de la gate (uniquement utile en dev local). Refuse explicitement
# d'être à TRUE en prod via un check au démarrage.
CHATBOT_GATE_DISABLED = (
    os.getenv("CHATBOT_GATE_DISABLED", "false").lower() == "true"
)
# TTL du cache d'unlock par user (en secondes). 5 min = bon compromis :
# si admin débloque un élève, il peut attendre max 5 min avant que la gate
# le laisse passer. Évite de hammerer Supabase à chaque message du bot.
UNLOCK_CACHE_TTL = int(os.getenv("UNLOCK_CACHE_TTL", "300"))

# Refus explicite : on n'autorise pas le bypass de la gate hors environnement
# de dev. La var est conçue pour le test local uniquement.
FLY_APP_NAME = os.getenv("FLY_APP_NAME")  # défini auto par Fly.io
if CHATBOT_GATE_DISABLED and FLY_APP_NAME:
    raise RuntimeError(
        "CHATBOT_GATE_DISABLED=true détecté en environnement Fly. "
        "Cette variable est réservée au dev local. Refuse de démarrer."
    )

# Refus explicite : sans la SUPABASE_ANON_KEY on ne peut pas appeler la RPC
# de gate. On laisse cependant passer en dev si CHATBOT_GATE_DISABLED=true.
if not SUPABASE_ANON_KEY and not CHATBOT_GATE_DISABLED:
    raise RuntimeError(
        "SUPABASE_ANON_KEY manquant. Indispensable pour appeler la RPC "
        "is_chatbot_unlocked. Renseigne-le dans .env (cf .env.example)."
    )

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


def get_bearer_token(
    authorization: Annotated[Optional[str], Header()] = None,
) -> str:
    """Extrait le JWT brut du header Authorization, sans le revalider.

    On a déjà `get_current_user` qui valide la signature ES256. Ici on
    veut juste réutiliser le même JWT pour le forward à Supabase (RPC
    `is_chatbot_unlocked`). FastAPI déduplique les appels au header
    Authorization, donc on peut déclarer les deux dépendances sans
    second appel réseau.
    """
    if not authorization or not authorization.lower().startswith("bearer "):
        # Cas théoriquement déjà couvert par get_current_user, mais on
        # double-check pour ne pas laisser passer un appel direct.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return authorization.split(" ", 1)[1].strip()


# ---------------------------------------------------------------------------
# Gate : 5/5 chapitres terminés OU admin override (RPC Supabase)
# ---------------------------------------------------------------------------

# Cache mémoire {user_id: (unlocked_bool, expires_at_epoch)}. On évite de
# hammerer Supabase à chaque message envoyé au bot. TTL configurable via
# UNLOCK_CACHE_TTL (5 min par défaut). Tradeoff : si l'admin débloque un
# élève en plein milieu d'une session, le débloque effectif peut prendre
# jusqu'à UNLOCK_CACHE_TTL secondes côté backend.
_unlock_cache: dict[str, tuple[bool, float]] = {}


def is_chatbot_unlocked_for_user(user_id: str, jwt_token: str) -> bool:
    """Appelle la RPC Supabase `is_chatbot_unlocked` pour l'utilisateur
    courant. Renvoie True si l'élève a accès au chatbot (5/5 chapitres
    terminés OU `chatbot_unlocked_by_admin = true`), False sinon.

    On forward le JWT user en `Authorization: Bearer …` ET on ajoute
    l'anon key dans le header `apikey` : c'est la convention REST
    Supabase pour les RPC. La fonction RPC utilise `auth.uid()` en
    interne (extrait du JWT) pour identifier l'élève — impossible donc
    de demander l'unlock d'un autre user.

    Comportement strict : en cas d'erreur réseau ou de réponse non-200,
    on retourne False (= bloqué). Vaut mieux refuser temporairement le
    chat qu'ouvrir une faille d'autorisation. L'erreur est logguée via
    le HTTPException levée en amont par le endpoint.
    """
    # Dev only bypass : utile pour développer en local sans avoir à
    # finir les 5 chapitres. Refus explicite en prod côté config (cf
    # check FLY_APP_NAME au démarrage).
    if CHATBOT_GATE_DISABLED:
        return True

    # Cache hit ?
    now = time.time()
    cached = _unlock_cache.get(user_id)
    if cached and cached[1] > now:
        return cached[0]

    # Cache miss : appel REST RPC Supabase.
    url = f"{SUPABASE_URL}/rest/v1/rpc/is_chatbot_unlocked"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt_token}",
        "apikey": SUPABASE_ANON_KEY or "",
    }
    try:
        resp = httpx.post(url, headers=headers, json={}, timeout=5.0)
    except httpx.HTTPError:
        # Réseau KO. On ne met PAS en cache (false négatif transitoire).
        return False

    if resp.status_code != 200:
        return False

    # La RPC retourne un bool brut (`true` / `false`).
    try:
        unlocked = bool(resp.json())
    except ValueError:
        return False

    _unlock_cache[user_id] = (unlocked, now + UNLOCK_CACHE_TTL)
    return unlocked


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


def rewrite_query_for_search(query: str) -> str:
    """Reformule la question utilisateur en query de recherche enrichie pour
    booster le rappel de l'embedding sur les questions courtes/vagues.

    Ex : "donne les différents LLM"
      → "types catégories LLM base instruction-tuned raisonnement multimodal vision"

    Le but : transformer une question vague (qui embedde mal sur ChromaDB)
    en une liste de mots-clés techniques alignés avec le vocabulaire du
    syllabus ISTQB GenAI. Coût : ~$0.0001 + ~300ms par requête /chat.

    Fail-soft : en cas d'erreur OpenAI ou de réponse vide, on retombe sur
    la query d'origine pour ne pas dégrader l'UX.
    """
    try:
        completion = openai_client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Tu reçois une question d'élève sur le syllabus ISTQB "
                        "GenAI. Tu dois produire une query de recherche pour "
                        "un moteur vectoriel.\n"
                        "RÈGLES STRICTES :\n"
                        "- REPRENDS d'abord les mots-clés EXACTS de la "
                        "question (ne traduis JAMAIS, ne reformule JAMAIS un "
                        "terme spécifique : 'IA fantôme' reste 'IA fantôme', "
                        "'RAG' reste 'RAG', 'prompt injection' reste "
                        "'prompt injection', etc.).\n"
                        "- AJOUTE ENSUITE 3 à 6 synonymes ou mots-clés "
                        "connexes du domaine ISTQB GenAI.\n"
                        "- Pas de phrase complète, juste des mots-clés "
                        "séparés par des espaces.\n"
                        "- Pas de ponctuation finale, pas de guillemets.\n"
                        "- En cas de doute sur un terme, GARDE-le tel quel "
                        "sans le remplacer.\n"
                        "- Réponds uniquement avec la query, rien d'autre.\n"
                        "Exemples :\n"
                        "Q: 'c'est quoi un LLM' → 'LLM grand modèle de "
                        "langage Transformer génératif pré-entraîné'\n"
                        "Q: 'donne les différents LLM' → 'différents LLM "
                        "types base instruction-tuned raisonnement "
                        "multimodal vision'\n"
                        "Q: 'IA fantôme' → 'IA fantôme shadow AI usage "
                        "non autorisé sécurité conformité confidentialité'"
                    ),
                },
                {"role": "user", "content": query},
            ],
            temperature=0,
            max_tokens=80,
        )
        rewritten = (completion.choices[0].message.content or "").strip()
        # Filet de sécurité : si l'API renvoie vide ou trop court, fallback.
        if len(rewritten) < 3:
            return query
        # Belt-and-suspenders : on préfixe la query originale même si le
        # rewriter est censé l'avoir reprise. Ça garantit que l'embedding
        # garde le bon biais sémantique même si le rewriter dérape (ex:
        # 'IA fantôme' interprété à tort en 'hallucination').
        return f"{query} {rewritten}"
    except Exception:
        return query


def retrieve_best_section(query: str):
    """V8 BEST-DISTANCE SECTION : top 20 chunks → groupés par section →
    on classe par **meilleur match** (distance min) plutôt que par nombre
    de chunks. Évite qu'une section longue (ex: 3.2 sécurité) noie une
    section courte mais ciblée (ex: 5.1.1 IA fantôme) juste parce qu'elle
    a plus de chunks dans la base. On garde le top-2 pour les questions
    transverses (ex: 'types LLM' = 1.1.3 + 1.1.4)."""
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
    dists = (
        results["distances"][0]
        if results.get("distances")
        else [float("inf")] * len(docs)
    )

    if not docs:
        return [], [], None

    section_groups: dict = {}
    for doc, meta, dist in zip(docs, metas, dists):
        key = (meta.get("chapter", "NA"), meta.get("section", "NA"))
        if key not in section_groups:
            section_groups[key] = {
                "docs": [],
                "meta": meta,
                "min_dist": dist,
            }
        else:
            section_groups[key]["min_dist"] = min(
                section_groups[key]["min_dist"], dist
            )
        section_groups[key]["docs"].append(doc)

    # Ranking par meilleur chunk de la section (distance min ascending).
    # Une section ultra-pertinente avec 1 chunk bat une section moyennement
    # pertinente avec 5 chunks.
    top_sections = sorted(
        section_groups.values(),
        key=lambda x: x["min_dist"],
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
    bearer_token: Annotated[str, Depends(get_bearer_token)],
):
    # Gate "5/5 chapitres terminés OU admin override". Défense en
    # profondeur : le frontend cache déjà le widget tant que cette RPC
    # ne renvoie pas true, mais quelqu'un qui appellerait /chat
    # directement (curl, repost depuis l'inspector…) doit aussi être
    # bloqué côté serveur. On répond 403 (pas 401) pour distinguer "JWT
    # valide mais pas autorisé" de "JWT invalide".
    if not is_chatbot_unlocked_for_user(user_id, bearer_token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Chatbot non débloqué. Termine les 5 chapitres du syllabus "
                "(ou demande à un admin de débloquer manuellement)."
            ),
        )

    # Mémoire : on garde les 10 derniers messages (5 échanges).
    history = req.history[-10:]

    search_query = build_search_query(req.question, history)
    # Query rewriter : enrichit la query pour le moteur vectoriel. Sans ça,
    # une question vague comme "donne les différents LLM" embedde mal et
    # rate les sections 1.1.3 / 1.1.4 qui contiennent la vraie réponse.
    search_query = rewrite_query_for_search(search_query)

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
