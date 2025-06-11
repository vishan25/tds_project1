# from fastapi import FastAPI, Request
# from pydantic import BaseModel
# import faiss
# import json
# import numpy as np
# from sentence_transformers import SentenceTransformer
# from typing import List
# import os

# INDEX_PATH = "/home/petpooja-1052/Downloads/project_of_Tds/tds_project1/faiss_index/index.faiss"
# METADATA_PATH = "/home/petpooja-1052/Downloads/project_of_Tds/tds_project1/faiss_index/metadata.jsonl"
# EMBED_MODEL = "all-MiniLM-L6-v2"
# TOP_K = 5

# # Load embedding model, index and metadata at startup
# print("🔁 Loading model, index, and metadata...")
# model = SentenceTransformer(EMBED_MODEL)
# index = faiss.read_index(INDEX_PATH)
# metadata = [json.loads(line) for line in open(METADATA_PATH, "r", encoding="utf-8")]

# app = FastAPI()

# class QueryInput(BaseModel):
#     question: str

# @app.post("/askQuestion")
# def ask_question(input_data: QueryInput):
#     query = input_data.question
#     embedding = model.encode([query], normalize_embeddings=True)
#     D, I = index.search(np.array(embedding, dtype="float32"), TOP_K)

#     relevant_chunks = [metadata[i]["text"] for i in I[0]]
#     context = "\n---\n".join(relevant_chunks)

#     # Simulated RAG (you can replace this with OpenAI or local LLM call)
#     answer = f"📚 **Context:**\n{context}\n\n🤖 **Answer:**\nBased on the above context, your question was: '{query}'."

#     return {"answer": answer}




