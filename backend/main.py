from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.rag import generate_answer, generate_summary


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="University Knowledge Assistant API",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",

        # Vite is currently running on 5174
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "University Knowledge Assistant API is running"
    }


# =========================================================
# ASK QUESTION
# =========================================================

@app.post("/ask")
def ask_question(data: dict):

    question = data.get("question", "").strip()

    if not question:

        return {
            "answer": "Please enter a question.",
            "sources": []
        }

    answer, results = generate_answer(question)

    sources = []

    for result in results:

        sources.append({
            "chunk_id": result["chunk_id"],
            "score": round(result["score"], 4)
        })

    return {
        "answer": answer,
        "sources": sources
    }


# =========================================================
# DOCUMENT SUMMARIZATION
# =========================================================

@app.post("/summarize")
def summarize_document():

    summary = generate_summary()

    return {
        "summary": summary
    }
