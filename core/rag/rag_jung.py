
# RAG MODULE FOR JUNG AGENT
# ./core/rag/rag_jung.py

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load model once (global, efficient)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load index + texts
index = faiss.read_index("rag/jung/jung.index")

with open("rag/jung/jung_texts.txt", "r", encoding="utf-8") as f:
    texts = f.read().split("\n---\n")


# -------------------------------
# RETRIEVE FUNCTION
# -------------------------------
def retrieve(query, k=3):
    """
    Returns top-k relevant chunks from Jung KB
    """

    # Convert query → embedding
    query_vec = model.encode([query])

    # Search FAISS
    D, I = index.search(np.array(query_vec), k)

    # Fetch corresponding texts
    results = [texts[i] for i in I[0] if i < len(texts)]
    
    if not results:
        return "No relevant Jungian context found."
    
    return "\n\n".join(results)


