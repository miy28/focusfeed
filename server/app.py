import os
from flask import Flask, send_from_directory, jsonify, request
from web.flask_web import visualizer
from core.orchestrator import fetch_articles
from flasgger import Swagger
import datetime

from recommender.recommender import SearchBar

app = Flask(__name__, static_folder='../web/root/dist')
app.register_blueprint(visualizer)
app.config['SWAGGER'] = {
    'title': 'My API',
    'uiversion': 3,
    'openapi': '3.0.2',
    'specs_route': '/apidocs/'  # This defines where your docs will be accessible
}
swagger = Swagger(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health Check Endpoint
    ---
    tags:
      - System
    responses:
      200:
        description: System health status
        schema:
          type: object
          properties:
            status:
              type: string
              description: Health status
              example: "healthy"
            timestamp:
              type: string
              description: Current timestamp
              example: "2025-04-28T12:00:00Z"
    """
    return jsonify({
        'status': 'healthy',
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/search', methods=['GET'])
def search():
    """
    Search Articles API
    ---
    tags:
      - Articles
    parameters:
      - name: query
        in: query
        description: Search query term
        required: false
        schema:
          type: string
          default: "Ukraine"
      - name: limit
        in: query
        description: Maximum number of results to return
        required: false
        schema:
          type: integer
          default: 10
    responses:
      200:
        description: List of articles matching the search criteria
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  articleId:
                    type: string
                    description: Unique identifier for the article
                  title:
                    type: string
                    description: Article title
                  snippet:
                    type: string
                    description: Brief excerpt from the article
                  publishDate:
                    type: string
                    description: Publication date
                  url:
                    type: string
                    description: Article URL
      400:
        description: Invalid request parameters
    """
    search_term = request.args.get('query', 'Ukraine')
    limit = request.args.get('limit', 10, type=int)
    
    try:
        search = SearchBar()
        top_articles = search.search_articles(key_phrase=search_term, top_n=limit)
        return jsonify(top_articles)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/search_multiple', methods=['GET'])
def search_multiple():
    """
    Search Articles API with Support for Multiple Keywords
    ---
    tags:
      - Articles
    parameters:
      - name: query
        in: query
        description: Search query term(s), comma-separated for multiple terms
        required: false
        schema:
          type: string
          default: "Ukraine, Trump"
      - name: limit
        in: query
        description: Maximum number of results to return per term
        required: false
        schema:
          type: integer
          default: 5
    responses:
      200:
        description: Articles matching the search criteria, organized by individual terms and merged results
        content:
          application/json:
            schema:
              type: object
              properties:
                individual_results:
                  type: object
                  description: Results grouped by search term
                merged_results:
                  type: array
                  items:
                    type: object
                    properties:
                      articleId:
                        type: string
                      title:
                        type: string
                      abstract:
                        type: string
                      url:
                        type: string
                      publishedAt:
                        type: string
                      keywordId:
                        type: string
                      keyword:
                        type: string
                      similarity_score:
                        type: number
      400:
        description: Invalid request parameters
    """
    search_term = request.args.get('query', 'Ukraine, Trump')
    limit = request.args.get('limit', 5, type=int)
    try:
        search = SearchBar()
        top_articles = search.search_articles(key_phrase=search_term, top_n=limit)
        return jsonify(top_articles)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)

# @app.route('/api/touch_db', methods=["POST"]) # stage 4
# def touch_sql():
#     # insert a feednote
#     word = request.json.get('word', '')
#     noteId, summary = touch_db(word)
#     if noteId == -1:
#         response = "Error: No articles found."
#     else:
#         response = f"Generated new FeedNote @ id {noteId}. {summary}"
#     return jsonify({'result': response})

