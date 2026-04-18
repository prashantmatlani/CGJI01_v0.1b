
# BASE RETRIEVER - ./core/rag/base_retrier.py

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

# Cache loaded indices (important for performance)
INDEX_CACHE = {}
TEXT_CACHE = {}


def load_agent_index(agent):

    if agent in INDEX_CACHE:
        return INDEX_CACHE[agent], TEXT_CACHE[agent]

    index_path = f"rag/{agent}/{agent}.index"
    text_path = f"rag/{agent}/{agent}_texts.txt"

    if not os.path.exists(index_path) or not os.path.exists(text_path):
        return None, []

    index = faiss.read_index(index_path)

    with open(text_path, "r", encoding="utf-8") as f:
        texts = f.read().split("\n---\n")

    INDEX_CACHE[agent] = index
    TEXT_CACHE[agent] = texts

    return index, texts


def retrieve(agent, query, k=3):

    index, texts = load_agent_index(agent)

    if index is None:
        return ""

    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec), k)

    results = [texts[i] for i in I[0] if i < len(texts)]

    return "\n\n".join(results)
