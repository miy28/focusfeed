from aggregator.nytimes_api import fetch_nytimes_articles
from user_preferences.categories import get_top_categories

import random

def fetch_articles():
    categories = get_top_categories(3)
    feed = []

    for category in categories:
        print(f"Fetching articles from category {category}")

        nytimes_articles = fetch_nytimes_articles(category)

        # add the other apis here once they're implemented

        if nytimes_articles:
            feed.append(random.choice(nytimes_articles).title)

    return feed

if __name__ == "__main__":
    from rich import print
    from rich.pretty import pprint
    print("[bold cyan]Welcome to FocusFeed homepage. Here is your custom news feed:[/bold cyan]")
    pprint(fetch_articles())