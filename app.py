import os
from dotenv import load_dotenv
from openai import OpenAI
import chromadb
import streamlit as st

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="istqb_knowledge")

st.set_page_config(
    page_title="Assistant Formation",
    page_icon="🎓"
)

st.title("Assistant Formation")
st.write("Besoin d’aide ? Pose ta question.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Pose ta question...")

if question:

    st.chat_message("user").write(question)

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # mémoire 5 échanges
    st.session_state.messages = st.session_state.messages[-10:]

    # ===== MEMORY LOCK =====
    implicit_follow_up_keywords = [
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
        "ça"
    ]

    last_assistant_message = ""

    for msg in reversed(st.session_state.messages):
        if msg["role"] == "assistant":
            last_assistant_message = msg["content"]
            break

    is_implicit_follow_up = any(
        keyword in question.lower()
        for keyword in implicit_follow_up_keywords
    )

    if is_implicit_follow_up and last_assistant_message:
        search_query = (
            last_assistant_message
            + "\n\nInstruction utilisateur : "
            + question
        )
    else:
        search_query = question

    question_embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=search_query
    ).data[0].embedding

    # ===== V6 MONO SECTION =====
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=12,
        where={"category": "syllabus"}
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    section_groups = {}

    for doc, meta in zip(documents, metadatas):

        section_key = (
            meta.get("chapter", "NA"),
            meta.get("section", "NA")
        )

        if section_key not in section_groups:
            section_groups[section_key] = {
                "docs": [],
                "meta": meta
            }

        section_groups[section_key]["docs"].append(doc)

    best_section = max(
        section_groups.values(),
        key=lambda x: len(x["docs"])
    )

    documents = best_section["docs"]
    primary_meta = best_section["meta"]

    context = "\n\n---\n\n".join(documents)

    sources = []

    for meta in metadatas:
        sources.append(
            f"{meta.get('category')} / {meta.get('source')}"
        )

    conversation_history = ""

    for msg in st.session_state.messages[-10:]:
        conversation_history += (
            f"{msg['role']}: {msg['content']}\n"
        )

    prompt = f"""
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

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1
    )

    answer = response.choices[0].message.content

    st.chat_message("assistant").write(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.expander("Sources syllabus (debug local)"):
        for source in sorted(set(sources)):
            st.write(source)