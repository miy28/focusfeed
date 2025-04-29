import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Any, Tuple, Optional, Union
from rich.pretty import pprint

from sql.constants import *

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
    
    def execute_procedure(self, procedure_call, params=None):
        try:
            if params:
                self.cursor.callproc(procedure_call.replace("CALL ", "").split("(")[0], params)
            else:
                self.cursor.callproc(procedure_call.replace("CALL ", "").split("(")[0])
            
            results = []
            for result in self.cursor.stored_results():
                results.extend(result.fetchall())
            
            return results
        except mysql.connector.Error as e:
            print(f"Error executing stored procedure: {e}")
            return []
    
    def execute_and_commit(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            return False

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
    
    def show_all_triggers(self):
        query = """
        SELECT TRIGGER_NAME, EVENT_MANIPULATION, EVENT_OBJECT_TABLE, ACTION_STATEMENT
        FROM information_schema.TRIGGERS 
        WHERE TRIGGER_SCHEMA = %s
        """
        triggers = self.fetch_all(query, (DATBASE,))
        
        if not triggers:
            print("No triggers found in the database.")
        else:
            print(f"Found {len(triggers)} triggers:")
            for trigger in triggers:
                print(f"\nName: {trigger['TRIGGER_NAME']}")
                print(f"Event: {trigger['EVENT_MANIPULATION']} ON {trigger['EVENT_OBJECT_TABLE']}")
                print(f"Statement: {trigger['ACTION_STATEMENT']}")
        
        return triggers
    
    def delete_all_triggers(self):
        query = """
        SELECT TRIGGER_NAME 
        FROM information_schema.TRIGGERS 
        WHERE TRIGGER_SCHEMA = %s
        """
        triggers = self.fetch_all(query, (DATBASE,))
        
        if not triggers:
            print("No triggers found to delete.")
            return True
        
        success = True
        deleted_count = 0
        
        for trigger in triggers:
            trigger_name = trigger['TRIGGER_NAME']
            drop_query = f"DROP TRIGGER IF EXISTS {trigger_name}"
            
            try:
                result = self.execute_query(drop_query)
                if result:
                    deleted_count += 1
                    print(f"Deleted trigger: {trigger_name}")
                else:
                    print(f"Failed to delete trigger: {trigger_name}")
                    success = False
            except Exception as e:
                print(f"Error deleting trigger {trigger_name}: {str(e)}")
                success = False
        
        print(f"Deleted {deleted_count} out of {len(triggers)} triggers.")
        return success

def create_article_stats_table():
    db_manager = DBManager(host=HOST, database=DATBASE, user=USER, password=PASSWORD)
    
    if not db_manager.connect():
        print("Failed to connect to the database")
        return False
    
    try:
        query = """
        CREATE TABLE IF NOT EXISTS ArticleStats (
            articleId INT PRIMARY KEY,
            likes_count INT DEFAULT 0,
            dislikes_count INT DEFAULT 0,
            FOREIGN KEY (articleId) REFERENCES Articles(articleId)
        );
        """
        success = db_manager.execute_query(query)
        
        if success:
            print("ArticleStats table created successfully!")
            return True
        else:
            print("Failed to create ArticleStats table")
            return False
            
    finally:
        db_manager.disconnect()
        print("Database connection closed")

    
if __name__ == "__main__":
    dbm = DBManager(host=HOST, database=DATBASE, user=USER, password=PASSWORD)
    tables = dbm.get_tables()
    for x in tables:
        pprint(x)
        pprint(dbm.get_columns(table_name=x))
    
    pprint(dbm.show_all_triggers())
    pprint(dbm.delete_all_triggers())



# OLD STUFF DONT USE THIS PYSQL IS FOR POSTGRES
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

#     with open("sql/feednotes_create.sql", "r", encoding="utf-8") as file:
#         sql_query = file.read().strip()

#     cursor.execute(sql_query)
#     conn.commit()

#     cursor.close()
#     conn.close()