from flask import Flask
from visualization.web_visualization import visualizer

def create_app():
    app = Flask(__name__)
    app.register_blueprint(visualizer)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
