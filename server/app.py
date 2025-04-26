import os
from flask import Flask, send_from_directory, jsonify, request
from web.flask_web import visualizer
from core.orchestrator import fetch_articles, stage_keyword
from sql.stage4 import touch_db

app = Flask(__name__, static_folder='../web/root/dist')
app.register_blueprint(visualizer)

''' serving static react frontend '''
@app.route('/')
def serve_index():
    return send_from_directory('../web/root/dist', 'index.html')

@app.route('/assets/<path:path>')
def serve_assets(path):
    return send_from_directory('../web/root/dist/assets', path) # filename '{path}'

''' backend apis for frontend '''
@app.route('/api/get_articles', methods=["GET"])
def get_articles():
    return jsonify(fetch_articles())

@app.route('/api/touch_db', methods=["POST"]) # stage 4
def touch_sql():
    # insert a feednote
    word = request.json.get('word', '')
    noteId, summary = touch_db(word)
    if noteId == -1:
        response = "Error: No articles found."
    else:
        response = f"Generated new FeedNote @ id {noteId}. {summary}"
    return jsonify({'result': response})
    
@app.route('api/log_interaction')
async def log_interaction(ait):
    keywords = ait.keywords
    for keyword in keywords:
        stage_keyword(keyword)

if __name__ == "__main__":
    # app = create_app()
    app.run(debug=True, port=5000)
