
# CONTEXT BUILDER - ./core/context_builder.py

from core.rag.rag_jung import retrieve
from core.tools.web_search import web_search

def should_use_web(query):
    trigger_words = ["what is", "who is", "define", "meaning", "latest"]
    return any(w in query.lower() for w in trigger_words)

def build_context(agent, query):

    # -----------------------------
    # RAG CONTEXT
    # -----------------------------
    rag_context = retrieve(query)

    # -----------------------------
    # WEB CONTEXT (only if needed)
    # -----------------------------
    web_context = ""

    if should_use_web(query) or len(rag_context.strip()) < 50:
        print("🌐 Using web fallback...")
        web_context = web_search(query) or ""

    # -----------------------------
    # COMBINED CONTEXT
    # -----------------------------
    combined = f"""
    {agent.upper()} KNOWLEDGE:
    {rag_context}

    REAL-WORLD CONTEXT:
    {web_context}
    """

    return combined.strip()