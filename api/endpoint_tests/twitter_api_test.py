import os
import requests
from dotenv import load_dotenv

load_dotenv()

TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")


# needs to fetch multiple sets of tweets for each pull (set to max of 10 for now)
def fetch_tweets(query: str = "SpaceX"):
    url = "https://api.twitter.com/2/tweets/search/recent"
    
    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    
    params = {"query": query, "max_results": 10}
    resp = requests.get(url, headers=headers, params=params)
    
    if not resp.ok:
        return {"error": f"Twitter API request failed: {resp.status_code}"}
    data = resp.json()
    return data.get("data", [])

if __name__ == "__main__":
    from rich.pretty import pprint
    pprint(fetch_tweets())
