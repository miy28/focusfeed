import os
import requests
from dotenv import load_dotenv

load_dotenv()

REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "Mozilla/5.0")

##
#reddit - for unauth reqs we have to use oauth but this is simple search for now
##

def fetch_reddit_posts(subreddit: str = "all", query: str = "SpaceX"):
    url = f"https://www.reddit.com/r/{subreddit}/search.json?q={query}&restrict_sr=1"
    headers = {"User-Agent": REDDIT_USER_AGENT}
    resp = requests.get(url, headers=headers)
    if not resp.ok:
        return {"error": f"Reddit API request failed: {resp.status_code}"}
    data = resp.json()

    posts = [child["data"] for child in data.get("data", {}).get("children", [])]
    return posts

if __name__ == "__main__":
    from rich.pretty import pprint
    pprint(fetch_reddit_posts())
