from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from rich import print
from dotenv import load_dotenv
 
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query : str) -> str:
    """
    Perform a web search using Tavily API, Returns titles, urls, and snippets.
    """
    # max_results=3 and snippet[:150] keeps tool output ~600 tokens,
    # preventing ITPM (7000/min) overflow on Groq free tier.
    results = tavily.search(query=query, max_results=3)

    out = []

    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:150]}\n"
        )

    return "\n----\n".join(out)

@tool
def scrape_url(url: str) -> str:
    """
    Scrape and return clean text content from a given URL for deep reading.
    """
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, 'html.parser')
        for tag in soup(['script', 'style', 'nav', 'footer']):
            tag.decompose()
        # 1500 chars (~375 tokens) keeps context well within the 7000 ITPM limit
        return soup.get_text(separator=" ", strip=True)[:1500]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
