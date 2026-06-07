import os
import re
import shutil
from dotenv import load_dotenv
from openai import OpenAI
import chromadb

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "istqb_knowledge"
# Phase 1 (backup) : on pointe sur corpus/genai pour préparer le multi-certif.
# Quand on ajoutera Foundation, ce sera corpus/foundation, etc.
DOCUMENTS_PATH = "./corpus/genai"

# Reset propre de la base
if os.path.exists(CHROMA_PATH):
    shutil.rmtree(CHROMA_PATH)

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)


def extract_chapter_from_filename(filename):
    match = re.search(r"chapitre[-_ ]?(\d+)", filename.lower())
    return f"Chapitre {match.group(1)}" if match else "Non identifié"


def split_by_sections(text):
    sections = []
    current_section = {
        "section": "Non identifiée",
        "title": "Introduction",
        "content": ""
    }

    lines = text.splitlines()

    for line in lines:
        section_match = re.match(r"^#{1,4}\s*(\d+(?:\.\d+)*)\s*[-—:]?\s*(.*)", line.strip())

        if section_match:
            if current_section["content"].strip():
                sections.append(current_section)

            current_section = {
                "section": section_match.group(1),
                "title": section_match.group(2).strip() or "Sans titre",
                "content": line + "\n"
            }
        else:
            current_section["content"] += line + "\n"

    if current_section["content"].strip():
        sections.append(current_section)

    return sections


def chunk_text(text, chunk_size=1800):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


for root, dirs, files in os.walk(DOCUMENTS_PATH):
    for filename in files:
        if filename.endswith(".md"):

            filepath = os.path.join(root, filename)
            category = os.path.basename(root)
            chapter = extract_chapter_from_filename(filename)

            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

            sections = split_by_sections(text)

            for section_index, section_data in enumerate(sections):
                chunks = chunk_text(section_data["content"])

                for chunk_index, chunk in enumerate(chunks):
                    embedding = client.embeddings.create(
                        model="text-embedding-3-small",
                        input=chunk
                    ).data[0].embedding

                    chunk_id = f"{category}-{filename}-section-{section_index}-chunk-{chunk_index}"

                    collection.add(
                        ids=[chunk_id],
                        embeddings=[embedding],
                        documents=[chunk],
                        metadatas=[{
                            "category": category,
                            "source": filename,
                            "chapter": chapter,
                            "section": section_data["section"],
                            "title": section_data["title"]
                        }]
                    )

                    print(
                        f"Ajouté : {category} / {filename} / {chapter} / Section {section_data['section']} / chunk {chunk_index}"
                    )

print("Base IA régénérée avec métadonnées chapitre/section.")