import pymysql
from llm.gemini import gemini

with open("db_credentials.txt", "r", encoding="utf-8") as file:
    creds = [line.strip() for line in file.readlines()]
host, user, password, database = creds

def touch_db(word: str):
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    cursor = conn.cursor()

    with open("sql/queries/stage4/rand_article.sql", "r", encoding="utf-8") as file:
        rand_article = file.read().strip()

    cursor.execute(rand_article, (word,))
    try:
        articleId, title, abstract = cursor.fetchone()
    except:
        return -1, ""

    with open("sql/queries/stage4/touch_feednote.sql", "r", encoding="utf-8") as file:
        touch_feednote = file.read().strip()

    summary = gemini(abstract)
    
    feednote = (
        102,
        articleId,
        title,
        summary
    )

    cursor.execute(touch_feednote, feednote) # create new feednote from article
    noteId = cursor.lastrowid

    conn.commit()
    
    cursor.close()
    conn.close()

    return noteId, summary
