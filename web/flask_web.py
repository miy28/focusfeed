from flask import Flask, Blueprint, jsonify, request, render_template
import requests
from core.core import aggregate_feed
from core.orchestrator import fetch_articles

# blueprint for frontend endpoints
visualizer = Blueprint("visualization", __name__)

@visualizer.route("/api/feed", methods=["GET"])
def get_feed():
    # pull query, def is "SpaceX"
    query = request.args.get("query", "SpaceX")
    
    # call aggregator
    feed_notes = aggregate_feed(query)
    
    # feednote dict conversion
    result = []
    for note in feed_notes:
        result.append({
            "title": note.title,
            "content": note.content,
            "url": note.url,
            "timestamp": note.timestamp,
            "source": note.source
        })
    
    #simple json output for now
    return jsonify(result)

@visualizer.route("/api/stage4")
def stage4_form():
    return render_template('stage4.html')

@visualizer.route("/api/stage4/touch_db", methods=["POST"])
def touch_sql():
    word = request.form['input']
    resp = requests.post('http://localhost:5000/api/touch_db', json={'word': word}) # call backend route
    ret = resp.json().get('result', 'Error')

    return ret

if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(visualizer)
    app.run(debug=True, port=5050)
