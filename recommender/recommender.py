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

