import os
from flask import Flask, send_from_directory, jsonify, request
from web.flask_web import visualizer
from core.orchestrator import fetch_articles
from flasgger import Swagger
import datetime

from recommender.recommender import SearchBar, TinderInteraction

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
    Search Articles API
    ---
    tags:
      - Articles
    parameters:
      - name: query
        in: query
        description: Search query term(s)
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
          default: 5
    responses:
      200:
        description: Articles matching the search criteria
        content:
          application/json:
            schema:
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
                  keyword:
                    type: string
                  viewCount:
                    type: integer
                  avgRating:
                    type: number
                  similarity_score:
                    type: number
      400:
        description: Invalid request parameters
    """
    search_term = request.args.get('query', 'Ukraine')
    limit = request.args.get('limit', 5, type=int)
    
    try:
        search = SearchBar()
        results = search.search_articles(key_phrase=search_term, top_n=limit)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/record_interaction', methods=['POST'])
def record_interaction():
    """
    Record User Interaction with Article API
    ---
    tags:
      - Interactions
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - articleId
              - interactionType
            properties:
              articleId:
                type: integer
                description: ID of the article interacted with
              interactionType:
                type: string
                enum: ['click', 'like', 'dislike', 'favorite', 'unfavorite']
                description: Type of interaction
    responses:
      200:
        description: Interaction recorded successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                message:
                  type: string
                articleStats:
                  type: object
                  properties:
                    articleId:
                      type: integer
                    likes_count:
                      type: integer
                    dislikes_count:
                      type: integer
      400:
        description: Invalid request parameters
      500:
        description: Server error recording interaction
    """
    try:
        data = request.get_json()
        
        if not data or 'articleId' not in data or 'interactionType' not in data:
            return jsonify({"success": False, "message": "Missing required fields"}), 400
        
        article_id = data['articleId']
        interaction_type = data['interactionType']
        
        valid_types = ['click', 'like', 'dislike', 'favorite', 'unfavorite']
        if interaction_type not in valid_types:
            return jsonify({
                "success": False, 
                "message": f"Invalid interaction type. Must be one of: {', '.join(valid_types)}"
            }), 400
        
        tinder = TinderInteraction()
        article_created = tinder.ensure_article_exists(article_id)
        if article_created is None: 
            return jsonify({
                "success": False,
                "message": f"Article with ID {article_id} doesn't exist and couldn't be created"
            }), 400
        
        tinder.record_interaction(article_id, interaction_type)
        stats = tinder.get_article_stats(article_id)

        return jsonify({
            "success": True,
            "message": f"Successfully recorded {interaction_type} for article {article_id}",
            "articleStats": stats if stats else {
                "articleId": article_id,
                "likes_count": 0,
                "dislikes_count": 0
            }
        })
        
    except Exception as e:
        # Log the error for debugging
        print(f"Error in record_interaction: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500

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

