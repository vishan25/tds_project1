import pandas as pd
import nltk
import os
import json
from nltk.tokenize import sent_tokenize
from tqdm import tqdm


CHUNK_SIZE = 300  
CHUNK_OVERLAP = 50  
OUTPUT_FILE = "all_chunks.jsonl"

tds_df = pd.read_csv("cleaned_tds_content.csv")         
disc_df = pd.read_csv("cleaned_discourse_posts.csv")    
tds_df["text"] = tds_df["title"].fillna("") + "\n" + tds_df["content"].fillna("")
disc_df["text"] = disc_df["topic_title"].fillna("") + "\n" + disc_df["content"].fillna("")

# Combine both
df = pd.concat([tds_df[["text"]], disc_df[["text"]]], ignore_index=True)

# Tokenize and chunk each text
def chunk_text(text, source_id):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""
    current_length = 0

    for sent in sentences:
        tokens = sent.split()
        if current_length + len(tokens) <= CHUNK_SIZE:
            current_chunk += " " + sent
            current_length += len(tokens)
        else:
            chunks.append(current_chunk.strip())
            # Start new chunk with overlap
            overlap_tokens = current_chunk.split()[-CHUNK_OVERLAP:]
            current_chunk = " ".join(overlap_tokens) + " " + sent
            current_length = len(current_chunk.split())

    if current_chunk:
        chunks.append(current_chunk.strip())

    return [{"chunk": c, "source_id": source_id} for c in chunks]

# Create all chunks
all_chunks = []
for i, row in tqdm(df.iterrows(), total=len(df)):
    all_chunks.extend(chunk_text(row["text"], i))

# Save to .jsonl
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for chunk in all_chunks:
        f.write(json.dumps(chunk) + "\n")

print(f"✅ Chunking complete: {len(all_chunks)} chunks saved to {OUTPUT_FILE}")
