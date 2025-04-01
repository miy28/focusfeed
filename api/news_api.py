import os
import requests
from dotenv import load_dotenv, find_dotenv
from core.data_models import ArticleIterator

load_dotenv(find_dotenv())

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_newsapi_articles(query: str = "SpaceX") -> list[ArticleIterator]:
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}"
    resp = requests.get(url)
    if not resp.ok:
        print(f"Error fetching NewsAPI data: {resp.status_code}")
        return []
    
    data = resp.json()
    articles = []

    # populate ArticleIterator w get req 
    for article in data.get("articles", []):
        note = ArticleIterator(
            title=article.get("title", "No Title"),
            desc=article.get("description", "No Content"),
            url=article.get("url", ""),
            timestamp=article.get("publishedAt", ""),
            source="NewsAPI",
            extra_data=article
        )
        articles.append(note)
    return articles

if __name__ == "__main__":
    from rich.pretty import pprint
    pprint(fetch_newsapi_articles())
