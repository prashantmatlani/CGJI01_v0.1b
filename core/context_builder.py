
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
