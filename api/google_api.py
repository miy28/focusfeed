import os
import requests
from dotenv import load_dotenv, find_dotenv
from core.data_models import ArticleIterator

load_dotenv(find_dotenv())

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def fetch_googleapi_articles(query: str = "SpaceX") -> list[ArticleIterator]:
    url = f"https://news.google.com/rss/search?q={query}&apiKey={GOOGLE_API_KEY}"
    resp = requests.get(url)
    if not resp.ok:
        print(f"Error fetching Google News data: {resp.status_code}")
        return []
    
    data = resp.json()
    articles = []

    # populate ArticleIterator w get req 
    for article in data.get("articles", []):
        note = ArticleIterator(
            title=article.get("title", "No Title"),
            desc=article.get("description", "No Content"),
            url=article.get("link", ""),
            timestamp=article.get("published", ""),
            source="GoogleAPI", 
            extra_data=article
        )
        articles.append(note)
    return articles

if __name__ == "__main__":
    from rich.pretty import pprint
    pprint(fetch_googleapi_articles())
