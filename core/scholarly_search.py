
from duckduckgo_search import DDGS
from core.scholarly_sources import SCHOLARLY_SOURCES

def scholarly_search(query, max_results=5):

    domains = []
    for category in SCHOLARLY_SOURCES.values():
        domains.extend(category)

    site_filter = " OR ".join([f"site:{d}" for d in domains])

    search_query = f"{query} ({site_filter})"

    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(search_query, max_results=max_results):
            results.append({
                "title": r["title"],
                "link": r["href"],
                "snippet": r["body"]
            })

    return results
