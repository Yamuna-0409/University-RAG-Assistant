from pathlib import Path


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

input_file = (
    BASE_DIR
    / "data"
    / "silver"
    / "andhra_university_cse_syllabus_clean.txt"
)

output_file = (
    BASE_DIR
    / "data"
    / "gold"
    / "chunks.txt"
)


# =========================================================
# READ CLEANED TEXT
# =========================================================

text = input_file.read_text(
    encoding="utf-8"
)


# =========================================================
# CHUNK SETTINGS
# =========================================================

chunk_size = 2000
overlap = 400


# =========================================================
# CREATE CHUNKS
# =========================================================

chunks = []

start = 0

while start < len(text):

    end = start + chunk_size

    chunk = text[start:end]

    if chunk.strip():
        chunks.append(chunk)

    start = end - overlap


# =========================================================
# SAVE CHUNKS
# =========================================================

output_file.write_text(
    "\n\n---CHUNK---\n\n".join(chunks),
    encoding="utf-8"
)


# =========================================================
# RESULT
# =========================================================

print(f"Created {len(chunks)} chunks")

print(f"Saved to: {output_file}")