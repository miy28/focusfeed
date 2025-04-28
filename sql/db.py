import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Any, Tuple, Optional, Union

host = ''
user = 'root'
password = ''
database = 'focusfeed-db-test'
class DBManager:
    def __init__(self, host: str, database: str, user: str, password: str, port: int = 3306):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None
        self.cursor = None

    def connect(self) -> bool:
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
        
        return False

    def disconnect(self) -> None:
        if self.connection and self.connection.is_connected():
            if self.cursor:
                self.cursor.close()
            self.connection.close()
            self.cursor = None
            self.connection = None

    def execute_query(self, query: str, params: tuple = None) -> bool:
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return False
            
            self.cursor.execute(query, params)
            self.connection.commit()
            return True
            
        except Error as e:
            print(f"Error executing query: {e}")
            return False

    def fetch_all(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        results = []
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return results
            
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            
        except Error as e:
            print(f"Error fetching data: {e}")
        
        return results

    def fetch_one(self, query: str, params: tuple = None) -> Optional[Dict[str, Any]]:
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return None
            
            self.cursor.execute(query, params)
            result = self.cursor.fetchone()
            return result
        
        except Error as e:
            print(f"Error fetching data: {e}")
            return None

    def insert(self, table: str, data: Dict[str, Any]) -> Optional[int]:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        try:
            if self.execute_query(query, tuple(data.values())):
                return self.cursor.lastrowid
            return None
            
        except Error as e:
            print(f"Error inserting data: {e}")
            return None
    
    def update(self, table: str, data: Dict[str, Any], condition: str, params: tuple = None) -> int:
        set_clause = ', '.join([f"{column} = %s" for column in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        
        all_params = tuple(data.values())
        if params:
            all_params += params
            
        try:
            if self.execute_query(query, all_params):
                return self.cursor.rowcount
            return 0
        except Error as e:
            print(f"Error updating data: {e}")
            return 0

    def table_exists(self, table_name: str) -> bool:
        query = "SHOW TABLES LIKE %s"
        result = self.fetch_one(query, (table_name,))
        return result is not None

    def create_table(self, table_name: str, columns: List[str]) -> bool:
        columns_def = ', '.join(columns)
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})"
        return self.execute_query(query)

    def execute_transaction(self, queries: List[Tuple[str, tuple]]) -> bool:
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return False
            
            self.connection.start_transaction()
            for query, params in queries:
                self.cursor.execute(query, params)
            
            self.connection.commit()
            return True
        except Error as e:
            self.connection.rollback()
            print(f"Transaction failed: {e}")
            return False

    def get_tables(self) -> List[str]:
        query = "SHOW TABLES"
        results = self.fetch_all(query)
        return [list(table.values())[0] for table in results] if results else []

    def get_columns(self, table_name: str) -> List[Dict[str, Any]]:
        query = f"DESCRIBE {table_name}"
        return self.fetch_all(query)


# import pymysql

# host = ''
# user = 'root'
# password = ''
# database = 'focusfeed-db-test'

# userId = 1

# def new_interaction(note):
#     conn = pymysql.connect(
#         host=host,
#         user=user,
#         password=password,
#         database=database
#     )

#     cursor = conn.cursor()

#     with open("sql/query_note.sql", "r", encoding="utf-8") as file:
#         sql_query = file.read().strip()

#     data = (
#         userId,
#         note.title,
#         note.keyword,
#         note.url,
#         # note.timestamp
#     )

#     cursor.execute(sql_query, data)
#     conn.commit()

#     cursor.close()
#     conn.close()

# def create_table():
#     conn = pymysql.connect(
#         host=host,
#         user=user,
#         password=password,
#         database=database
#     )

#     cursor = conn.cursor()

#     with open("sql/feednotes_create.sql", "r", encoding="utf-8") as file:
#         sql_query = file.read().strip()

#     cursor.execute(sql_query)
#     conn.commit()

#     cursor.close()
#     conn.close()