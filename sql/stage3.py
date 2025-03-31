import time
import random
import nltk
from nltk.corpus import words as nltk_words
from datetime import datetime
import pymysql

from aggregator.nytimes_api import fetch_nytimes_articles
from aggregator.google_api import fetch_googleapi_articles
from aggregator.news_api import fetch_newsapi_articles
from user_preferences.categories import get_top_categories
from llm.gemini import gemini

with open("db_credentials.txt", "r", encoding="utf-8") as file:
    creds = [line.strip() for line in file.readlines()]
host, user, password, database = creds

def init_tables():

    print(creds)

    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    cursor = conn.cursor()
    
    with open("sql/queries/articles_create.sql", "r", encoding="utf-8") as file:
        articles_create = file.read().strip()

    with open("sql/queries/feednotes_create.sql", "r", encoding="utf-8") as file:
        feednotes_create = file.read().strip()

    with open("sql/queries/keywords_create.sql", "r", encoding="utf-8") as file:
        keywords_create = file.read().strip()

    with open("sql/queries/articlesKeywords_create.sql", "r", encoding="utf-8") as file:
        articleskeywords_create = file.read().strip()

    with open("sql/queries/interactions_create.sql", "r", encoding="utf-8") as file:
        interactions_create = file.read().strip()

    # cursor.execute(articles_create)
    # cursor.execute(feednotes_create)
    # cursor.execute(keywords_create)
    # cursor.execute(articleskeywords_create)
    cursor.execute(interactions_create)
    conn.commit()

    cursor.close()
    conn.close()

def fill_tables():
    '''
    do like 100 real unique articles
    then loop over each and insert them 10 times into the db
    just need to satisfy 1000 rows "you may use auto-generated data. "
    '''

    # nltk.download('genesis')
    word_bank = nltk.corpus.genesis.words()

    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    cursor = conn.cursor()

    with open("sql/queries/feednotes_insert.sql", "r", encoding="utf-8") as file:
        feednotes_insert = file.read().strip()

    with open("sql/queries/articles_insert.sql", "r", encoding="utf-8") as file:
        articles_insert = file.read().strip()
    
    # with open("sql/news_insert.sql", "r", encoding="utf-8") as file:
    #     news_insert = file.read().strip()

    # with open("sql/google_insert.sql", "r", encoding="utf-8") as file:
    #     google_insert = file.read().strip()

    with open("sql/queries/keywords_insert.sql", "r", encoding="utf-8") as file:
        keywords_insert = file.read().strip()

    with open("sql/queries/keywords_get.sql", "r", encoding="utf-8") as file:
        keywords_get = file.read().strip()

    with open("sql/queries/articlesKeywords_insert.sql", "r", encoding="utf-8") as file:
        articlesKeywords_insert = file.read().strip()

    # fill Articles, Keywords, articlesKeywords, FeedNotes
    for userId in range(60):
        query_word = random.choice(word_bank)
        nytimes_notes = fetch_nytimes_articles(query_word) # get list of notes
        # news_notes = fetch_newsapi_articles(query_word)
        # google_notes = fetch_googleapi_articles(query_word)

        for note in nytimes_notes:
            
            mysql_datetime = datetime.strptime(note.timestamp, "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d %H:%M:%S")

            nytimes_entry = ( # Articles schema
                note.title[:255],
                note.desc[:255],
                note.url[:255],
                mysql_datetime
            )
            cursor.execute(articles_insert, nytimes_entry)
            articleId = cursor.lastrowid # get the pushed row's id for relationship table

            for keyword in note.keywords: # create a relation for every keyword from the article
                word = keyword["value"]
                cursor.execute(keywords_insert, (word))
                cursor.execute(keywords_get, (word))
                keywordId = cursor.fetchone()[0]
                cursor.execute(articlesKeywords_insert, (articleId, keywordId))
                print("inserted a keyword: ", keywordId, "", word, flush=True)

            feednotes_entry = ( # FeedNotes schema
                userId,
                articleId,
                note.title[:255],
                gemini(note.desc + note.snippet)[:300]
            )
            cursor.execute(feednotes_insert, feednotes_entry) # we're gonna replace this later. this is not how we create feedNotes.
        conn.commit()
        time.sleep(20) # api request limit

    conn.commit()

    cursor.close()
    conn.close()

    print("Success.")

'''
4 'advanced' queries
The queries should each involve at least two of the following SQL concepts:
    Join multiple relations
    SET Operators
    Aggregation via GROUP BY
    Subqueries that cannot be easily replaced by a join. 
'''

# (1)
# advanced query that gets the count of every category, then orders these counts by descending
# replaces the get_top_categories method in categories.py (maybe we depracate the whole ml feature for this)

if __name__ == "__main__":
    init_tables()
    # fill_tables()
