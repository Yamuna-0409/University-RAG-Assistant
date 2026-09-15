from pathlib import Path
from sentence_transformers import SentenceTransformer
import json
import numpy as np

# Load embeddings
input_file = Path("data/gold/embeddings.json")

data = json.loads(
    input_file.read_text(encoding="utf-8")
)

print(f"Loaded {len(data)} chunks")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def search(query, top_k=3):

    # Convert user question into embedding
    query_embedding = model.encode(query)

    results = []

    for item in data:

        chunk_embedding = np.array(item["embedding"])

        # Cosine similarity
        similarity = np.dot(query_embedding, chunk_embedding) / (
            np.linalg.norm(query_embedding)
            * np.linalg.norm(chunk_embedding)
        )

        results.append({
            "chunk_id": item["chunk_id"],
            "text": item["text"],
            "score": float(similarity)
        })

    # Sort by highest similarity
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]


# Test query
query = input("Enter your question: ")

results = search(query)

print("\nTop matching chunks:\n")

for result in results:

    print("=" * 80)
    print(f"Chunk ID: {result['chunk_id']}")
    print(f"Similarity Score: {result['score']:.4f}")
    print(result["text"][:1000])