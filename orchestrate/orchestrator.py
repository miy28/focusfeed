import random
import pymysql

from aggregator.nytimes_api import fetch_nytimes_articles
from user_preferences.categories import get_top_categories
from sql.db import new_interaction, create_table

def fetch_articles():
    categories = get_top_categories(3)
    feed = []

    for category in categories:
        print(f"Fetching articles from category {category}")

        nytimes_notes = fetch_nytimes_articles(category) # list of notes

        # add the other apis here once they're implemented

        if nytimes_notes:
            note = random.choice(nytimes_notes)
            feed.append(note.title) # display a few random articles from user's top k categories
            new_interaction(note) # send this to the db (simulate an interaction)

    return feed

if __name__ == "__main__":
    # create_table()
    from rich import print
    from rich.pretty import pprint
    print("[bold cyan]Welcome to FocusFeed homepage. Here is your custom news feed:[/bold cyan]")
    pprint(fetch_articles())