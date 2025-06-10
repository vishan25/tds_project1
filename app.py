import json
import faiss
import os
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd

CHUNK_FILE = "/home/petpooja-1052/Downloads/project_of_Tds/tds_project1/combined_chunks.csv"
INDEX_FILE = "faiss_index/index.faiss"
METADATA_FILE = "faiss_index/metadata.jsonl"
EMBED_MODEL = "all-MiniLM-L6-v2"

def load_chunks(path):
    print("📦 Loading chunks from CSV...")
    df = pd.read_csv(path)
    return [{"text": row["chunk"]} for _, row in df.iterrows()]

def save_metadata(metadata, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for record in metadata:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

def build_index(chunks, model):
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=64, normalize_embeddings=True)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatIP(dim)  # Cosine similarity via inner product
    index.add(np.array(embeddings, dtype="float32"))

    return index, embeddings

def main():
    print("📦 Loading chunks from CSV...")
    chunks = load_chunks(CHUNK_FILE)

    print(f"🧠 Loading embedding model: {EMBED_MODEL}")
    model = SentenceTransformer(EMBED_MODEL)

    print("🔧 Building FAISS index...")
    index, _ = build_index(chunks, model)

    print(f"💾 Saving FAISS index to: {INDEX_FILE}")
    os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)
    faiss.write_index(index, INDEX_FILE)

    print(f"💾 Saving metadata to: {METADATA_FILE}")
    save_metadata(chunks, METADATA_FILE)

    print("✅ Index and metadata saved successfully.")

if __name__ == "__main__":
    main()
