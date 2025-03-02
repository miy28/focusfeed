import os
import requests
from dotenv import load_dotenv
from aggregator.data_models import FeedNote

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_newsapi_articles(query: str = "SpaceX") -> list[FeedNote]:
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}"
    resp = requests.get(url)
    if not resp.ok:
        print(f"Error fetching NewsAPI data: {resp.status_code}")
        return []
    
    data = resp.json()
    articles = []

    # populate feednote w get req 
    for article in data.get("articles", []):
        note = FeedNote(
            title=article.get("title", "No Title"),
            content=article.get("description", "No Content"),
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
