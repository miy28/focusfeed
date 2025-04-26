import random
import time
import sys
import pyfiglet
from pyfiglet import Figlet
import pymysql

from api.nytimes_api import fetch_nytimes_articles
from core.data_models import ArticleIterator, FeedNote
from recommender.categories import get_top_categories
from sql.db import new_interaction, create_table
from llm.gemini import gemini
from recommender.recommender import model_w2v, get_embedding
from recommender.data_models import get_pkl, save_pkl, VDB_PATH, VQ_PATH, MAX_WINDOW_LEN

categories_vocab = {} # (for debugging) holds user history.

def fetch_articles(query):
    '''
    fetch new articles, might not be in sql db
    gets at most 10 articles
    '''
    articles = fetch_nytimes_articles(query)

    if articles:
        return articles
    
def lookup_articles(query1, query2, N=10):
    '''
    look up articles in sql db. two keywords improves specificity of the search.
    gets at most 10 articles
    '''

    articles = []
    
    # (run sql lookup get max 10 items. of articles that have both query1 and query2 as keywords
    # make it return title, desc, url, timestamp, source, keywords, snippet, extra_data)
    sql_response = None

    for article in sql_response:
        note = ArticleIterator(
            title=article[0],
            desc=article[1],
            url=article[2],
            timestamp=article[3],
            source=article[4],
            keywords=article[5],
            snippet=article[6],
            extra_data=article[7]
        )
        articles.append(note)

    return articles

def stage_keyword(keyword, vq): # backend -> middle
    embedding = get_embedding(model_w2v, keyword)
    vq.append((embedding, keyword))

def generate_feednote(ait):
    title = ait.title
    summary = gemini(ait.desc) # rag
    url = ait.url

    note = FeedNote(
        title=title,
        summary=summary,
        url=url,
    )

    return note

def generate_feed(mood):
    feed = [] # list of FeedNotes

    

    return feed

if __name__ == "__main__":
    print("arnav")