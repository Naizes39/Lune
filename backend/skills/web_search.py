import asyncio
from ddgs import DDGS


async def web_search(query: str, max_results: int = 5) -> dict:
    """
    Searches the web for the given query and returns a list of results.
    Use this tool when the user asks about current events, recent information,
    or anything that requires up-to-date knowledge beyond your training data.

    Args:
        query (str): The search query, in natural language.
        max_results (int): Maximum number of results to return (default 5).

    Returns:
        dictionary with keys:
        - results: list of dicts, each with "title", "url", "snippet"
        - error: present only if the search failed (string describing what went wrong)
    """
    if not query or not query.strip():
        return {"error": "Empty search query.", "results": []}

    try:
        results = await asyncio.to_thread(
            lambda: list(DDGS().text(query, max_results=max_results))
        )
        formatted = [
            {
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", ""),
            }
            for r in results
        ]
        return {"results": formatted}
    except Exception as e:
        return {"error": f"Search failed: {e}", "results": []}