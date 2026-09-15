from pathlib import Path

input_file = Path("data/bronze/andhra_university_cse_syllabus.txt")
output_file = Path("data/silver/andhra_university_cse_syllabus_clean.txt")

text = input_file.read_text(encoding="utf-8")

# Remove unnecessary blank lines
lines = text.splitlines()

clean_lines = []

for line in lines:
    line = line.strip()

    if line:
        clean_lines.append(line)

clean_text = "\n".join(clean_lines)

output_file.write_text(clean_text, encoding="utf-8")

print("Text cleaning completed!")
print(f"Saved to: {output_file}")