import os
import re
import pandas as pd
from pathlib import Path

INPUT_DIR = "tds_pages_md"
OUTPUT_CSV = "cleaned_tds_content.csv"

def strip_yaml_and_clean_markdown(text):
    # Remove YAML front matter
    text = re.sub(r"^---.*?---\s*", "", text, flags=re.DOTALL)
    # Remove images: ![alt](url)
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    # Remove links: [text](url)
    text = re.sub(r"\[([^\]]+)\]\(.*?\)", r"\1", text)
    # Remove bold/italic/code formatting: **text**, *text*, `code`
    text = re.sub(r"[*_`]", "", text)
    # Remove headings and excess whitespace
    text = re.sub(r"#+\s*", "", text)
    text = re.sub(r"\n+", "\n", text)
    return text.strip()

rows = []

for md_file in Path(INPUT_DIR).glob("*.md"):
    with open(md_file, "r", encoding="utf-8") as f:
        raw = f.read()
        cleaned = strip_yaml_and_clean_markdown(raw)
        rows.append({
            "filename": md_file.name,
            "content": cleaned
        })

df = pd.DataFrame(rows)
df.to_csv(OUTPUT_CSV, index=False)

print(f"✅ Cleaned content saved to: {OUTPUT_CSV}")