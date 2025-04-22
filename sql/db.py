import pymysql

host = ''
user = 'root'
password = ''
database = 'focusfeed-db-test'

userId = 1

def new_interaction(note):
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    cursor = conn.cursor()

    with open("sql/query_note.sql", "r", encoding="utf-8") as file:
        sql_query = file.read().strip()

    data = (
        userId,
        note.title,
        note.keyword,
        note.url,
        # note.timestamp
    )

    cursor.execute(sql_query, data)
    conn.commit()

    cursor.close()
    conn.close()

def create_table():
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    cursor = conn.cursor()

    with open("sql/feednotes_create.sql", "r", encoding="utf-8") as file:
        sql_query = file.read().strip()

    cursor.execute(sql_query)
    conn.commit()

    cursor.close()
    conn.close()