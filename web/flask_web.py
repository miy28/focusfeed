# web/flask_web.py

import logging
import requests
from flask import Blueprint, jsonify, request, render_template
from core.core import aggregate_feed

logger = logging.getLogger(__name__)
visualizer = Blueprint("visualization", __name__)


@visualizer.route("/feed", methods=["GET"])
def get_feed():
    """
    Front-end feed endpoint
    """
    query = request.args.get("query", "SpaceX")
    try:
        feed = aggregate_feed(query)
    except Exception:
        logger.exception(f"aggregate_feed failed for query={query!r}")
        feed = []
    return jsonify(feed)


@visualizer.route("/stage4")
def stage4_form():
    return render_template('stage4.html')


@visualizer.route("/stage4/touch_db", methods=["POST"])
def touch_sql():
    word = request.form.get('input', '')
    resp = requests.post(
        'http://localhost:5000/api/touch_db',
        json={'word': word}
    )
    return resp.json().get('result', 'Error')
