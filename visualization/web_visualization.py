from flask import Flask, Blueprint, jsonify, request
from aggregator.core import aggregate_feed

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

if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(visualizer)
    app.run(debug=True, port=5050)
