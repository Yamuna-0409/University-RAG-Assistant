from pathlib import Path
from sentence_transformers import SentenceTransformer
import json

# Input and output files
input_file = Path("data/gold/chunks.txt")
output_file = Path("data/gold/embeddings.json")

# Read chunks
text = input_file.read_text(encoding="utf-8")

# Split chunks
chunks = text.split("\n\n---CHUNK---\n\n")

# Remove empty chunks
chunks = [chunk.strip() for chunk in chunks if chunk.strip()]

print(f"Total chunks: {len(chunks)}")

# Load embedding model
print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Creating embeddings...")

# Convert each chunk into a numerical vector
embeddings = model.encode(
    chunks,
    show_progress_bar=True
)

# Store chunks + embeddings
data = []

for i in range(len(chunks)):
    data.append({
        "chunk_id": i,
        "text": chunks[i],
        "embedding": embeddings[i].tolist()
    })

# Save as JSON
output_file.write_text(
    json.dumps(data),
    encoding="utf-8"
)

print("Embeddings created successfully!")
print(f"Saved to: {output_file}")