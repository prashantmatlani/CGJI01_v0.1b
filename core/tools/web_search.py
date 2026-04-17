
# ./core/web_search.py

import os
from tavily import TavilyClient

client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

def web_search(query, max_results=3):
    try:
        response = client.search(
            query=query,
            search_depth="basic",
            max_results=max_results
        )

        results = []

        for r in response.get("results", []):
            results.append({
                "title": r.get("title"),
                "content": r.get("content"),
                "url": r.get("url")
            })

        #return results
        return "\n\n".join(results)

    except Exception as e:
        print("❌ Web search error:", e)
        return []