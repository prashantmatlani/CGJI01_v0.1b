

#CORE RETRIEVAL AUGMENTED GENERATION — core/rag.py

import chromadb
from sentence_transformers import SentenceTransformer

# init once
client = chromadb.Client()
collection = client.get_or_create_collection(name="jung_kb")

model = SentenceTransformer("all-MiniLM-L6-v2")


def add_documents(docs):
    embeddings = model.encode(docs).tolist()

    collection.add(
        documents=docs,
        embeddings=embeddings,
        ids=[str(i) for i in range(len(docs))]
    )


def retrieve_relevant_chunks(query, k=3):

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k
    )

    return "\n".join(results["documents"][0])