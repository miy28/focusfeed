from sql.db import DBManager
from sql.constants import *
from rich.pretty import pprint
import difflib

class SearchBar:
	def __init__(self):
		self.db_manager = DBManager(host=HOST, database=DATBASE, user=USER, password=PASSWORD)
	
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
	def find_articles(self, key_phrase: str, num_keywords=5, max_articles=5):
		"""
		1) Collect a list of all the keywords from the Keywords table
		2) Match the key_phrase with keywords to get the top N keywords
		3) Use the keywordId to get the articleId through articlesKeywords table
		4) Return up to 5 articles in JSON format
		"""
		if not self.db_manager.connect():
			raise Exception("Cannot connect to database")
		
		# Step 1: Get all keywords from the Keywords table
		keywords_query = "SELECT keywordId, keyword FROM Keywords"
		keywords_results = self.db_manager.fetch_all(keywords_query, params=None)

		if not keywords_results:
			return {"articles": [], "message": "No keywords found in database"}
		
		# Create a list of (keywordId, keyword, similarity_score)
		keyword_matches = []
		key_phrase_lower = key_phrase.lower()
		
		for keyword_row in keywords_results:
			keyword_id = keyword_row['keywordId']
			keyword = keyword_row['keyword']
			
			# Calculate similarity using SequenceMatcher
			similarity = difflib.SequenceMatcher(None, key_phrase_lower, keyword.lower()).ratio()
			
			# Boost score if key_phrase contains the keyword or vice versa
			if key_phrase_lower in keyword.lower() or keyword.lower() in key_phrase_lower:
				similarity += 0.3
				
			keyword_matches.append((keyword_id, keyword, similarity))
		
		# Sort by similarity score in descending order and take top N
		keyword_matches.sort(key=lambda x: x[2], reverse=True)
		top_keywords = keyword_matches[:num_keywords]
		
		if not top_keywords:
			return {"articles": [], "message": "No matching keywords found"}
		
		# Step 3: Get article IDs from articlesKeywords table based on top keywords
		top_keyword_ids = [str(kw[0]) for kw in top_keywords]
		placeholders = ','.join(['?'] * len(top_keyword_ids))
		# return top_keyword_ids

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

