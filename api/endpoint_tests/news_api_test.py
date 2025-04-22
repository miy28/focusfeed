import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news_articles(query: str = "SpaceX"): #fixed q for now

    # query url
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}"
    
    resp = requests.get(url)
    if not resp.ok:
        return {"error": f"NewsAPI request failed: {resp.status_code}"}
    data = resp.json()
    return data.get("articles", [])

if __name__ == "__main__":
    from rich.pretty import pprint
    pprint(fetch_news_articles())
