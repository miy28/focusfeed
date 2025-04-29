from sql.db import DBManager
from sql.constants import *
from rich.pretty import pprint
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

class SearchBar:
    def __init__(self):
        self.db_manager = DBManager(host=HOST, database=DATBASE, user=USER, password=PASSWORD)
        
    def semantic_search(self, articles_list, key_phrase, top_n=5):
        unique_articles = {}
        search_texts = []
        article_map = {}  
        
        article_index = 0
        for article in articles_list:
            article_id = article['articleId']
            article_url = article['url']
            
            article_key = f"{article_id}_{article_url}"
            
            if article_id in unique_articles or article_url in [a['url'] for a in unique_articles.values()]:
                continue
                
            unique_articles[article_id] = article
            combined_text = f"{article['title']} {article['keyword']}"
            search_texts.append(combined_text)
            article_map[len(search_texts) - 1] = article_id 
        
        if not search_texts:
            return []
            
        all_texts = [key_phrase] + search_texts
        
        vectorizer = TfidfVectorizer(stop_words='english')
        try:
            tfidf_matrix = vectorizer.fit_transform(all_texts)
        except ValueError:
            return []
        
        key_phrase_vector = tfidf_matrix[0:1]
        article_vectors = tfidf_matrix[1:]
        similarities = cosine_similarity(key_phrase_vector, article_vectors)[0]
        
        article_similarities = []
        for i, score in enumerate(similarities):
            article_id = article_map[i]
            article_similarities.append((unique_articles[article_id], score))
        
        article_similarities.sort(key=lambda x: x[1], reverse=True)
        top_articles = article_similarities[:top_n]
        
        result = []
        for article, score in top_articles:
            article_copy = article.copy()
            article_copy['similarity_score'] = float(score)
            result.append(article_copy)
            
        return result
    
    def search_articles(self, key_phrase, top_n=5):
        if not self.db_manager.connect():
            raise Exception("Cannot connect to database")
        
        query = """
            SELECT a.articleId, a.title, a.abstract, a.url, a.publishedAt, k.keywordId, k.keyword
            FROM Articles a
            JOIN articlesKeywords ak ON a.articleId = ak.articleId
            JOIN Keywords k ON ak.keywordId = k.keywordId
            ORDER BY a.articleId, k.keywordId
        """
        articles_list = self.db_manager.fetch_all(query)
        results = self.semantic_search(articles_list, key_phrase, top_n)
        return results

class TinderInteraction:
    def __init__(self):
        self.db_manager = DBManager(host=HOST, database=DATBASE, user=USER, password=PASSWORD)
        
    def setup_article_stats_trigger(self):
        check_query = """
        SELECT TRIGGER_NAME FROM information_schema.TRIGGERS 
        WHERE TRIGGER_SCHEMA = %s AND TRIGGER_NAME = 'update_article_stats'
        """
        result = self.db_manager.fetch_one(check_query, (DATBASE,))
        
        if result:
            print("Trigger already exists, dropping it first")
            drop_query = "DROP TRIGGER IF EXISTS update_article_stats"
            self.db_manager.execute_query(drop_query)
                
        trigger_query = """
        CREATE TRIGGER update_article_stats
        AFTER INSERT ON Interactions
        FOR EACH ROW
        BEGIN
            DECLARE article_id INT;
            
            IF NEW.interactionType IN ('like', 'dislike') THEN
                SET article_id = NEW.noteId;
                
                IF article_id IS NOT NULL THEN
                    INSERT INTO ArticleStats 
                        (articleId, likes_count, dislikes_count)
                    VALUES 
                        (article_id, 
                        IF(NEW.interactionType = 'like', 1, 0),
                        IF(NEW.interactionType = 'dislike', 1, 0))
                    ON DUPLICATE KEY UPDATE
                        likes_count = likes_count + IF(NEW.interactionType = 'like', 1, 0),
                        dislikes_count = dislikes_count + IF(NEW.interactionType = 'dislike', 1, 0);
                END IF;
            END IF;
        END
        """
        
        try:
            # Create the trigger
            success = self.db_manager.execute_query(trigger_query)
            if success:
                print("Trigger created successfully")
                return True
            else:
                print("Failed to create trigger")
                return False
        except Exception as e:
            print(f"Error setting up trigger: {str(e)}")
            return False
      
    def record_interaction(self, note_id, interaction_type):
        query = """
        INSERT INTO Interactions (userId, noteId, timestamp, interactionType, interactionDuration) 
        VALUES (1, %s, NOW(), %s, 3.2)
        """
        self.db_manager.execute_query(query, (note_id, interaction_type))
    
    def get_user_interactions(self, user_id=1):
        query = "SELECT * FROM Interactions WHERE userId = %s"
        return self.db_manager.fetch_all(query, (user_id,))
    
    def get_all_article_stats(self):
        query = """
        SELECT * FROM ArticleStats
        """
        return self.db_manager.fetch_all(query)
    
    def get_article_stats(self, article_id):
        query = """
        SELECT * FROM ArticleStats WHERE articleId = %s
        """
        return self.db_manager.fetch_one(query, (article_id,))
    
    def get_popular_articles(self, limit=10):
        query = """
        SELECT a.*, s.likes_count, s.dislikes_count
        FROM Articles a
        JOIN ArticleStats s ON a.articleId = s.articleId
        ORDER BY s.likes_count DESC
        LIMIT %s
        """
        return self.db_manager.fetch_all(query, (limit,))
    
    def get_articles_with_stats(self):
        query = """
        SELECT 
            a.articleId, 
            a.title, 
            a.abstract, 
            a.url, 
            a.publishedAt,
            IFNULL(s.likes_count, 0) as likes_count,
            IFNULL(s.dislikes_count, 0) as dislikes_count,
            (IFNULL(s.likes_count, 0) - IFNULL(s.dislikes_count, 0)) as net_score
        FROM 
            Articles a
        LEFT JOIN 
            ArticleStats s ON a.articleId = s.articleId
        ORDER BY 
            net_score DESC, a.publishedAt DESC
        """
        return self.db_manager.fetch_all(query)

    def ensure_article_exists(self, article_id):
        check_query = "SELECT 1 FROM Articles WHERE articleId = %s"
        result = self.db_manager.fetch_one(check_query, (article_id,))
        if result:
            return True # article exists
        return False

class Recommender:
	def __init__():
		pass

	def run_search():
		pass

	

# gcloud auth login
# gcloud sql connect focusfeed-db --user=root
# gcloud sql connect focusfeed-db --user=root --password=gargalicious

# USE focusfeed-db-test;
# SHOW TABLES;


# query = f"SELECT * FROM Articles LIMIT 1"
# 		results = self.db_manager.fetch_all(query, params=None)
# 		pprint(results)

# 		query = f"SELECT * FROM articlesKeywords LIMIT 1"
# 		results = self.db_manager.fetch_all(query, params=None)
# 		pprint(results)

# 		query = f"SELECT * FROM Keywords LIMIT 1"
# 		results = self.db_manager.fetch_all(query, params=None)
# 		pprint(results)


# 		cols1 = self.db_manager.get_columns(table_name="Articles")
# 		cols2 = self.db_manager.get_columns(table_name="articlesKeywords")
# 		cols3 = self.db_manager.get_columns(table_name="Keywords")
# 		pprint(cols1)
# 		pprint(cols2)
# 		pprint(cols3)
# 		self.db_manager.disconnect()
# 		# # this function needs to take a key phrase query the articles
# 		# pass


# /focusfeed/get_top_feed_notes/{item}
# /focusfeed/get_top_feed_notes/{SpaceX}
# {
# 	{
# 		feed1
# 	},
# 	{
# 		feed2
# 	},
# 	...

# }

