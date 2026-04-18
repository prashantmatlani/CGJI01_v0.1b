

# CONTEXT BUILDER - ./core/context_builder.py

from core.rag.base_retriever import retrieve
from core.tools.web_search import web_search


def should_use_web(query):
    trigger_words = ["what is", "who is", "define", "meaning", "latest"]
    return any(w in query.lower() for w in trigger_words)


def build_context(agent, query):

    rag_context = retrieve(agent, query)

    web_context = ""
    
    # Only trigger web search if query looks factual / unknown
    if len(rag_context.strip()) < 50:
        try:
            results = search_web(query)
            web_context = "\n".join(results)
        except:
            web_context = ""


    combined = f"""
    {agent.upper()} KNOWLEDGE:
    {rag_context}
    
    REAL-WORLD CONTEXT:
    {web_context}
    """
    
    #return combined.strip()
    return combined


"""
from core.scholarly_search import scholarly_search
from core.content_extractor import extract_text

CACHE = {}

def build_scholarly_context(query):

    if query in CACHE:
        return CACHE[query]

    results = scholarly_search(query)

    context_blocks = []

    for r in results:
        text = extract_text(r["link"])
        if text:
            context_blocks.append(
                f"Source: {r['title']}\n{text}\n"
            )

    context = "\n\n".join(context_blocks[:3])

    CACHE[query] = context

    return context
"""
