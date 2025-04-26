import os
import sys
import requests
from dotenv import load_dotenv, find_dotenv
from core.data_models import ArticleIterator

load_dotenv(find_dotenv())
NY_TIMES_KEY = os.getenv("NY_TIMES_KEY")

def fetch_nytimes_articles(query: str = "SpaceX") -> list[ArticleIterator]:
    url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}&api-key={NY_TIMES_KEY}"
    resp = requests.get(url)
    if not resp.ok:
        print(f"\n\nError fetching NYTimes data: Code {resp.status_code} (Probably time-out.)\n")
        sys.stdout.write('\033[F\033[F\033[F\033[F') # ANSI (move cursor up thrice)
        return []
    
    data = resp.json()
    articles = []

    # populate ArticleIterator w data
    for doc in data.get("response", {}).get("docs", []):
        note = ArticleIterator(
            title=doc.get("headline", {}).get("main", "No Title"),
            desc=doc.get("abstract", "No Content"),
            url=doc.get("web_url", ""),
            timestamp=doc.get("pub_date", ""),
            source="NYTimes",
            # keyword=doc.get("keyword", {}).get("name", "No Keyword"),
            keywords=doc.get("keywords", "No Keyword"),
            snippet=doc.get("snippet", "No Snippet"),
            extra_data=doc
        )
        articles.append(note)
    
    return articles

if __name__ == "__main__":
    from rich.pretty import pprint
    pprint(fetch_nytimes_articles())
