import os
from flask import Flask, send_from_directory, jsonify, request
from web.flask_web import visualizer
from core.orchestrator import fetch_articles
from flasgger import Swagger
import datetime

from recommender.recommender import Search

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

@app.route('/api/search/', methods=['GET'])
def search():
    searchObj = Search()
    

if __name__ == "__main__":
    app.run(debug=True, port=5000)



# @app.route('/api/touch_db', methods=["POST"]) # stage 4
# # def touch_sql():
# #     # insert a feednote
# #     word = request.json.get('word', '')
# #     noteId, summary = touch_db(word)
# #     if noteId == -1:
# #         response = "Error: No articles found."
# #     else:
# #         response = f"Generated new FeedNote @ id {noteId}. {summary}"
# #     return jsonify({'result': response})

