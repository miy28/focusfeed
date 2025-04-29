from sql.db import DBManager
from sql.constants import *
from rich.pretty import pprint
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

"""
Find relevant articles based on keyword matching.
1) Collect a list of all the keywords from the Keywords table
2) Match the key_phrase with keywords to get the top N keywords
3) Use the keywordId to get the articleId through articlesKeywords table
4) Return up to 5 articles in JSON format
Args:
	key_phrase (str): The search phrase to match against keywords
	num_keywords (int, optional): Number of top matching keywords to use. Defaults to 5.
	max_articles (int, optional): Maximum number of articles to return. Defaults to 5.
Returns:
	dict: JSON formatted results with articles
"""
class SearchBar:
	def __init__(self, phrase: str):
		self.db_manager = DBManager(host=HOST, database=DATBASE, user=USER, password=PASSWORD)
		self.key_phrase = phrase
	
	def build_nested_json(self, output_file="articles_data.json"):		
		if not self.db_manager.connect():
			raise Exception("Cannot connect to database")
		
		# Fetch all data from tables
		articles_query = "SELECT articleId, title, abstract, url, publishedAt FROM Articles"
		articles_results = self.db_manager.fetch_all(articles_query)
		
		keywords_query = "SELECT keywordId, keyword FROM Keywords"
		keywords_results = self.db_manager.fetch_all(keywords_query)
		
		article_keywords_query = "SELECT articleId, keywordId FROM articlesKeywords"
		article_keywords_results = self.db_manager.fetch_all(article_keywords_query)
		
		# Create lookup dictionaries
		articles_dict = {}
		for article in articles_results:
			articles_dict[article['articleId']] = {
				"articleId": article['articleId'],
				"title": article['title'],
				"abstract": article['abstract'],
				"url": article['url'],
				"publishedAt": article['publishedAt'],
				"keywords": []
			}
		
		keywords_dict = {}
		for keyword in keywords_results:
			keywords_dict[keyword['keywordId']] = {
				"keywordId": keyword['keywordId'],
				"keyword": keyword['keyword'],
				"articles": []
			}
		
		# Build relationships
		for relation in article_keywords_results:
			article_id = relation['articleId']
			keyword_id = relation['keywordId']
			
			# Skip if article or keyword doesn't exist
			if article_id not in articles_dict or keyword_id not in keywords_dict:
				continue
			
			# Add keyword to article
			articles_dict[article_id]['keywords'].append({
				"keywordId": keyword_id,
				"keyword": keywords_dict[keyword_id]['keyword']
			})
			
			# Add article to keyword
			keywords_dict[keyword_id]['articles'].append(article_id)
		
		# Build the final structure
		result = {
			"articles": list(articles_dict.values()),
			"keywords": list(keywords_dict.values())
		}
		
		# Add metadata
		result["metadata"] = {
			"total_articles": len(articles_dict),
			"total_keywords": len(keywords_dict),
			"total_relationships": len(article_keywords_results),
			"generated_at": self.db_manager.fetch_one("SELECT datetime('now') as timestamp")['timestamp']
		}
		
		# Write to file
		with open(output_file, 'w', encoding='utf-8') as f:
			json.dump(result, f, indent=2, ensure_ascii=False)
		
		print(f"JSON data written to {output_file}")
		return result

	def get_articleIds(self): 
		query = "SELECT * FROM articlesKeywords"
		article_ids_results = self.db_manager.fetch_all(query, params=None)
		return article_ids_results
	
	def get_keywords(self):
		query = "SELECT * FROM Keywords"
		article_keyword_results = self.db_manager.fetch_all(query, params=None)
		return article_keyword_results
	
	def get_keyword_results(self):
		keywords_query = "SELECT keywordId, keyword FROM Keywords"
		keywords_results = self.db_manager.fetch_all(keywords_query, params=None)
		if not keywords_results:
			return {"articles": [], "message": "No keywords found in database"}
		keywords_dict = {item['keywordId']: item['keyword'] for item in keywords_results}
		return keywords_dict

	def find_articles(self, num_keywords=5, max_articles=5):
		if not self.db_manager.connect():
			raise Exception("Cannot connect to database")

		all_keywords = self.get_keyword_results()


		# Create a list containing the key_phrase and all keywords
		# all_texts = [self.key_phrase] + keywords

		# Create TF-IDF vectors
		vectorizer = TfidfVectorizer(stop_words='english')
		try:
			tfidf_matrix = vectorizer.fit_transform(all_texts)
		except ValueError:
			# Handle empty or all-stop-word input
			return {"articles": [], "message": "Invalid input for text analysis"}
		
		# Calculate similarity between key_phrase and each keyword
		key_phrase_vector = tfidf_matrix[0:1]
		keyword_vectors = tfidf_matrix[1:]
		similarities = cosine_similarity(key_phrase_vector, keyword_vectors)[0]
		
		# Create list of (keywordId, keyword, similarity_score)
		keyword_matches = [(keyword_ids[i], keywords[i], similarities[i]) for i in range(len(keywords))]
		
		# Sort by similarity score in descending order and take top N
		keyword_matches.sort(key=lambda x: x[2], reverse=True)
		top_keywords = keyword_matches[:num_keywords]
		return top_keywords
		
		if not top_keywords:
			return {"articles": [], "message": "No matching keywords found"}
		
		# Step 3: Get article IDs from articlesKeywords table based on top keywords
		top_keyword_ids = [str(kw[0]) for kw in top_keywords]
		placeholders = ','.join(['?'] * len(top_keyword_ids))
		
		article_ids_query = f"""
			SELECT DISTINCT articleId 
			FROM articlesKeywords 
			WHERE keywordId IN ({placeholders})
		"""
		
		article_ids_results = self.db_manager.fetch_all(article_ids_query, params=top_keyword_ids)
		
		if not article_ids_results:
			return {"articles": [], "message": "No articles found for the matched keywords"}
		
		# Get unique article IDs
		article_ids = [str(result['articleId']) for result in article_ids_results]
		
		# Step 4: Get article details from Articles table
		placeholders = ','.join(['?'] * len(article_ids))
		articles_query = f"""
			SELECT articleId, title, abstract, url, publishedAt 
			FROM Articles 
			WHERE articleId IN ({placeholders})
			LIMIT {max_articles}
		"""
		
		articles_results = self.db_manager.fetch_all(articles_query, params=article_ids)
		
		# Format articles as a list of dictionaries
		articles = []
		for article in articles_results:
			articles.append({
				"articleId": article['articleId'],
				"title": article['title'],
				"abstract": article['abstract'],
				"url": article['url'],
				"publishedAt": article['publishedAt']
			})
		
		# Return results as JSON
		return {
			"articles": articles,
			"matched_keywords": [{"keywordId": kw[0], "keyword": kw[1], "score": float(kw[2])} for kw in top_keywords],
			"total_matches": len(article_ids),
			"returned_articles": len(articles)
		}



	def find_articles_v1(self, num_keywords=5, max_articles=5):
		"""
		1) Collect a list of all the keywords from the Keywords table
		2) Match the key_phrase with keywords to get the top N keywords
		3) Use the keywordId to get the articleId through articlesKeywords table
		4) Return up to 5 articles in JSON format
		"""
		if not self.db_manager.connect():
			raise Exception("Cannot connect to database")
				
		keywords_query = "SELECT keywordId, keyword FROM Keywords"
		keywords_results = self.db_manager.fetch_all(keywords_query, params=None)
		if not keywords_results:
			return {"articles": [], "message": "No keywords found in database"}
		
		keyword_matches = []
		key_phrase_lower = self.key_phrase.lower()
		for keyword_row in keywords_results:
			keyword_id = keyword_row['keywordId']
			keyword = keyword_row['keyword']
			similarity = difflib.SequenceMatcher(None, key_phrase_lower, keyword.lower()).ratio()
			if key_phrase_lower in keyword.lower() or keyword.lower() in key_phrase_lower:
				similarity += 0.3
			keyword_matches.append((keyword_id, keyword, similarity))
		
		keyword_matches.sort(key=lambda x: x[2], reverse=True)
		top_keywords = keyword_matches[:num_keywords]
		if not top_keywords:
			return {"articles": [], "message": "No matching keywords found"}
		
		top_keyword_ids = [str(kw[0]) for kw in top_keywords]
		return top_keyword_ids
		placeholders = ','.join(['?'] * len(top_keyword_ids))
		article_ids_query = f"""
			SELECT DISTINCT articleId 
			FROM articlesKeywords 
			WHERE keywordId IN ({placeholders})
		"""
	
		article_ids_results = self.db_manager.fetch_all(article_ids_query, params=top_keyword_ids)
		if not article_ids_results:
			return {"articles": [], "message": "No articles found for the matched keywords"}
		return article_ids_results
		
		# Get unique article IDs
		article_ids = [str(result['articleId']) for result in article_ids_results]
		
		# Step 4: Get article details from Articles table
		placeholders = ','.join(['?'] * len(article_ids))
		articles_query = f"""
			SELECT articleId, title, abstract, url, publishedAt 
			FROM Articles 
			WHERE articleId IN ({placeholders})
			LIMIT {max_articles}
		"""
		
		articles_results = self.db_manager.fetch_all(articles_query, params=article_ids)
		
		# Format articles as a list of dictionaries
		articles = []
		for article in articles_results:
			articles.append({
				"articleId": article['articleId'],
				"title": article['title'],
				"abstract": article['abstract'],
				"url": article['url'],
				"publishedAt": article['publishedAt']
			})
		
		# Return results as JSON
		return {
			"articles": articles,
			"matched_keywords": [{"keywordId": kw[0], "keyword": kw[1], "score": kw[2]} for kw in top_keywords],
			"total_matches": len(article_ids),
			"returned_articles": len(articles)
		}
    
    


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

