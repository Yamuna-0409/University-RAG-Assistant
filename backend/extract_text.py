from pypdf import PdfReader
from pathlib import Path

input_file = Path("data/raw/andhra_university_cse_syllabus.pdf")
output_file = Path("data/bronze/andhra_university_cse_syllabus.txt")

reader = PdfReader(input_file)

text = ""

for page in reader.pages:
    page_text = page.extract_text()

    if page_text:
        text += page_text + "\n"

output_file.write_text(text, encoding="utf-8")

print("PDF text extraction completed!")
print(f"Saved to: {output_file}")