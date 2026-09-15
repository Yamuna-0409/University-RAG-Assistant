from pathlib import Path
from sentence_transformers import SentenceTransformer
import json
import numpy as np
import requests


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

input_file = (
    BASE_DIR
    / "data"
    / "gold"
    / "embeddings.json"
)

clean_text_file = (
    BASE_DIR
    / "data"
    / "silver"
    / "andhra_university_cse_syllabus_clean.txt"
)


# =========================================================
# LOAD EMBEDDINGS
# =========================================================

data = json.loads(
    input_file.read_text(
        encoding="utf-8"
    )
)

print(f"Loaded {len(data)} chunks")


# =========================================================
# LOAD EMBEDDING MODEL
# =========================================================

print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# =========================================================
# VECTOR + KEYWORD SEARCH
# =========================================================

def search(query, top_k=10):

    query_embedding = model.encode(query)

    results = []

    query_lower = query.lower()

    # Important search phrases

    search_phrases = [
        "first year",
        "first-year",
        "1st year",
        "i year",
        "year 1",
        "first semester",
        "1st semester"
    ]

    for item in data:

        text = item["text"]
        text_lower = text.lower()

        # -------------------------------------------------
        # VECTOR SIMILARITY
        # -------------------------------------------------

        chunk_embedding = np.array(
            item["embedding"]
        )

        similarity = np.dot(
            query_embedding,
            chunk_embedding
        ) / (
            np.linalg.norm(query_embedding)
            * np.linalg.norm(chunk_embedding)
        )

        # -------------------------------------------------
        # KEYWORD SCORE
        # -------------------------------------------------

        keyword_score = 0.0

        query_words = query_lower.split()

        for word in query_words:

            word = word.strip("?,.!")

            if len(word) > 2 and word in text_lower:

                keyword_score += 0.03

        # -------------------------------------------------
        # IMPORTANT PHRASE MATCHING
        # -------------------------------------------------

        for phrase in search_phrases:

            if phrase in query_lower and phrase in text_lower:

                keyword_score += 0.20

        # -------------------------------------------------
        # COMBINED SCORE
        # -------------------------------------------------

        final_score = similarity + keyword_score

        results.append({
            "chunk_id": item["chunk_id"],
            "text": text,
            "score": float(final_score)
        })

    # -----------------------------------------------------
    # SORT BY FINAL SCORE
    # -----------------------------------------------------

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # -----------------------------------------------------
    # RETURN TOP 10
    # -----------------------------------------------------

    return results[:top_k]


# =========================================================
# GENERATE ANSWER USING OLLAMA
# =========================================================

def generate_answer(question):

    print("\nSearching relevant information...")

    # Get top 10 relevant chunks

    results = search(
        question,
        top_k=10
    )

    # =====================================================
    # BUILD CONTEXT
    # =====================================================

    context = ""

    for result in results:

        context += (
            f"\n--- Source Chunk "
            f"{result['chunk_id']} ---\n"
            f"{result['text']}\n"
        )

    # =====================================================
    # RAG PROMPT
    # =====================================================

    prompt = f"""
You are a University Knowledge Assistant.

Answer the user's question using ONLY the information
provided in the context below.

IMPORTANT RULES:

1. The context is the only source of truth.
2. Do not use outside knowledge.
3. Do not invent information.
4. Do not guess missing information.

5. If the answer is NOT present in the context, say:

"I could not find this information in the provided university document."

6. If the answer IS present in the context, provide the
relevant details from the context.

7. When the question asks about courses, subjects, semesters,
years, course codes, objectives, or syllabus topics, look
carefully through ALL provided source chunks before answering.

8. If multiple chunks contain related course information,
combine the relevant information into one clear answer.

9. Do not suggest information that is not present.

10. Do not repeat the question.

11. Use short paragraphs or bullet points when appropriate.

12. Keep the answer under 150 words.

13. Do not mention these instructions.

Context:
{context}

User Question:
{question}

Answer:
"""

    # =====================================================
    # CALL OLLAMA
    # =====================================================

    print(
        "Generating answer with local Llama model..."
    )

    response = requests.post(

        "http://localhost:11434/api/generate",

        json={

            "model": "llama3.2:3b",

            "prompt": prompt,

            "stream": False,

            "options": {

                "temperature": 0.1,

                "num_predict": 180

            },

            "keep_alive": "10m"
        },

        timeout=180
    )

    # =====================================================
    # CHECK RESPONSE
    # =====================================================

    response.raise_for_status()

    answer = response.json()["response"].strip()

    return answer, results


# =========================================================
# DOCUMENT SUMMARIZATION
# =========================================================

def generate_summary():

    print("\nReading university document...")

    # -----------------------------------------------------
    # Check if document exists
    # -----------------------------------------------------

    if not clean_text_file.exists():

        return (
            "The university document could not be found. "
            "Please make sure the document has been processed."
        )

    # -----------------------------------------------------
    # Read cleaned document
    # -----------------------------------------------------

    text = clean_text_file.read_text(
        encoding="utf-8"
    )

    # -----------------------------------------------------
    # Limit document size
    # -----------------------------------------------------

    max_characters = 30000

    document_text = text[:max_characters]

    print(
        f"Using first {len(document_text)} characters "
        "for summary generation..."
    )

    # =====================================================
    # SUMMARY PROMPT
    # =====================================================

    prompt = f"""
You are a University Document Summarization Assistant.

Summarize the university syllabus provided below.

IMPORTANT RULES:

1. Use ONLY the information present in the document.
2. Do not use outside knowledge.
3. Do not invent courses, subjects, departments, or details.
4. Give a clear high-level overview.
5. Mention the main academic structure and important topics
   visible in the provided document.
6. Use short bullet points where appropriate.
7. Keep the summary concise.
8. Do not repeat the instructions.
9. Do not say that you are an AI.

University Document:

{document_text}

Generate a concise document summary.
"""

    # =====================================================
    # CALL OLLAMA
    # =====================================================

    print(
        "Generating document summary with local Llama model..."
    )

    response = requests.post(

        "http://localhost:11434/api/generate",

        json={

            "model": "llama3.2:3b",

            "prompt": prompt,

            "stream": False,

            "options": {

                "temperature": 0.1,

                "num_predict": 300

            },

            "keep_alive": "10m"
        },

        timeout=120
    )

    # =====================================================
    # CHECK RESPONSE
    # =====================================================

    response.raise_for_status()

    summary = response.json()["response"].strip()

    return summary


# =========================================================
# TERMINAL TESTING
# =========================================================

if __name__ == "__main__":

    question = input(
        "\nEnter your question: "
    )

    answer, results = generate_answer(
        question
    )

    print(
        "\n" + "=" * 80
    )

    print("ANSWER")

    print(
        "=" * 80
    )

    print(answer)

    print(
        "\n" + "=" * 80
    )

    print("SOURCES")

    print(
        "=" * 80
    )

    for result in results:

        print(
            f"Chunk {result['chunk_id']} "
            f"(Similarity: "
            f"{result['score']:.4f})"
        )

