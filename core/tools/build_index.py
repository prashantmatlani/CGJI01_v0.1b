
# ./build_index.py

import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def build_index(folder):
    texts = []

    # Read all files
    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        if file.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                texts.append(content)

    if not texts:
        raise Exception(f"No text files found in {folder}")

    # Create embeddings
    embeddings = model.encode(texts)

    # Convert to numpy
    embeddings = np.array(embeddings).astype("float32")

    # Build FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    return index, texts


# -----------------------
# RUN
# -----------------------

folder_path = "kb/jung"

# create directory "kb" if it doesn't exist
#if not os.path.exists("kb"):
    #raise Exception(f"Folder not found: {folder}")
#    os.makedirs("kb", exist_ok=True)

index, texts = build_index(folder_path)

os.makedirs("rag/jung", exist_ok=True)

# Save index
faiss.write_index(index, "rag/jung/jung.index")

# Save raw texts
with open("rag/jung/jung_texts.txt", "w", encoding="utf-8") as f:
    f.write("\n---\n".join(texts))

print("✅ Index + texts saved successfully.")

