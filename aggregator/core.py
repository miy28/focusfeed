from aggregator.nytimes_api import fetch_nytimes_articles
from aggregator.news_api import fetch_newsapi_articles

def aggregate_feed(query: str = "SpaceX"): #query will be user defined in the future
    feed_notes = []
    
    # NYTimes pull
    try:
        nytimes_notes = fetch_nytimes_articles(query)
        feed_notes.extend(nytimes_notes)
    except Exception as e:
        print(f"Error aggregating NYTimes data: {e}")
    
    # NewsAPI pull
    try:
        newsapi_notes = fetch_newsapi_articles(query)
        feed_notes.extend(newsapi_notes)
    except Exception as e:
        print(f"Error aggregating NewsAPI data: {e}")
    
    # Add more 
    
    return feed_notes

if __name__ == "__main__":
    from rich.pretty import pprint
    pprint(aggregate_feed("SpaceX"))
