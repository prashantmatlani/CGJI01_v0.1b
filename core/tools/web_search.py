
# ./core/tools/web_search.py

import os
from tavily import TavilyClient

client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))


def web_search(query, max_results=3):
    """
    Performs web search and returns formatted context string.
    Also logs sources for debugging in HF logs.
    """

    try:
        response = client.search(
            query=query,
            search_depth="basic",
            max_results=max_results
        )

        results = response.get("results", [])

        if not results:
            print(f"🌐 No web results found for query: '{query}'")
            return ""

        formatted_chunks = []

        for r in results:
            title = r.get("title", "")
            content = r.get("content", "")
            url = r.get("url", "")

            # ✅ LOG EACH RESULT (THIS IS WHAT YOU WANT)
            print(f'🌐 Found info for client query: "{query}" at: {url}')

            # ✅ FORMAT FOR LLM CONTEXT
            chunk = f"""
                SOURCE: {title}
                URL: {url}
                CONTENT: {content}
                """
            formatted_chunks.append(chunk.strip())

        # ✅ FINAL CONTEXT STRING (USED BY AGENT)
        return "\n\n---\n\n".join(formatted_chunks)

    except Exception as e:
        print("❌ Web search error:", e)
        return ""