import os
import requests
import feedparser
from dotenv import load_dotenv

load_dotenv()

def fetch_google_news(query: str = "SpaceX"): #fixed query
    
    # goog news url format
    url = f"https://news.google.com/rss/search?q={query}"
    
    resp = requests.get(url)
    if not resp.ok:
        return {"error": f"Google News RSS request failed: {resp.status_code}"}
    feed = feedparser.parse(resp.content)
    articles = []
    for entry in feed.entries:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.get("published", "N/A")
        })
    return articles

if __name__ == "__main__":
    from rich.pretty import pprint
    pprint(fetch_google_news())
