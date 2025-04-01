import requests
import os
from rich.pretty import pprint
from dotenv import load_dotenv

load_dotenv()

NY_TIMES_KEY = os.getenv("NY_TIMES_KEY")
NY_TIMES_SECRET = os.getenv("NY_TIMES_SECRET")

def fetch_some_articles():
    query = "SpaceX"
    url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}&api-key={NY_TIMES_KEY}"
    resp = requests.get(url)
    if not resp.ok:
        return {"error" : f"{url} concern"}
    data = resp.json()
    return (data['response']['docs']).keys()

if __name__ == "__main__":
    pprint(fetch_some_articles())