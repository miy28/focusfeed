# from flask import Flask, Blueprint, jsonify, request
# from api.nytimes_api import fetch_nytimes_articles
# from api.news_api import fetch_newsapi_articles
# from api.google_api import fetch_googleapi_articles

# def aggregate_feed(query: str = "SpaceX"): #query will be user defined in the future
#     feed_notes = []
    
#     # NYTimes pull
#     try:
#         nytimes_notes = fetch_nytimes_articles(query)
#         feed_notes.extend(nytimes_notes)
#     except Exception as e:
#         print(f"Error aggregating NYTimes data: {e}")
    
#     # NewsAPI pull
#     try:
#         newsapi_notes = fetch_newsapi_articles(query)
#         feed_notes.extend(newsapi_notes)
#     except Exception as e:
#         print(f"Error aggregating NewsAPI data: {e}")

#     # GoogleNews pull

#     try:
#         googleapi_notes = fetch_googleapi_articles(query)
#         feed_notes.extend(googleapi_notes)
#     except Exception as e:
#         print(f"Error aggregating GoogleNews data: {e}")
    
#     # Add more 
    
#     return feed_notes

# def get_feed():
#     # pull query, def is "SpaceX"
#     # query = request.args.get("query", "SpaceX")
    
#     # call aggregator
#     feed_notes = aggregate_feed("SpaceX")
    
#     # feednote dict conversion
#     result = []
#     for note in feed_notes:
#         result.append({
#             "title": note.title,
#             "content": note.content,
#             "url": note.url,
#             "timestamp": note.timestamp,
#             "source": note.source
#         })
    
#     #simple json output for now
#     return jsonify(result)

# if __name__ == "__main__":
#     from rich.pretty import pprint
#     # pprint(aggregate_feed("SpaceX"))
#     # print("here")
#     app = Flask(__name__)
    
#     with app.app_context():
#         print(get_feed())


# core/core.py

import logging
from typing import List, Dict

from api.nytimes_api import fetch_nytimes_articles
from api.news_api import fetch_newsapi_articles
from api.google_api import fetch_googleapi_articles

logger = logging.getLogger(__name__)
# (somewhere in your app startup you should configure logging.basicConfig)

SOURCE_FUNCS = [
    ("NYTimes",   fetch_nytimes_articles),
    ("NewsAPI",   fetch_newsapi_articles),
    ("GoogleNews", fetch_googleapi_articles),
]

def aggregate_feed(query: str = "SpaceX") -> List[Dict]:
    """
    Pull from multiple news sources and return a unified list of dicts:
      { title, content, url, timestamp, source }
    """
    feed: List[Dict] = []

    for source_name, fn in SOURCE_FUNCS:
        try:
            notes = fn(query)  # each note has .title, .content, .url, .timestamp
            for n in notes:
                feed.append({
                    "title":     n.title,
                    "content":   n.content,
                    "url":       n.url,
                    "timestamp": n.timestamp,
                    "source":    source_name
                })
        except Exception:
            logger.exception(f"Failed to fetch from {source_name!r}")

    return feed
