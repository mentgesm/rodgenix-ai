from flask import Flask
from flask_cors import CORS
import pymysql
import os


# Define the static folder path relative to app.py
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend'))

# Initialize Flask app with proper static folder
app = Flask(__name__, static_folder=frontend_path)

@app.route("/")
def index():
    """Serve the landing page."""
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:filename>")
def serve_static(filename):
    """Serve any file in the frontend directory."""
    return send_from_directory(app.static_folder, filename)


from customers import customers_bp
from quotes import quotes_bp
from orders import orders_bp
from payments import payments_bp
from photos import photos_bp
from user_interactions import user_interactions_bp
from compatibility import compatibility_bp
from forecasts import forecasts_bp
from nlp_queries import nlp_queries_bp
from ai_models import ai_models_bp
from inventory import inventory_bp


# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS globally

# Register Blueprints
app.register_blueprint(customers_bp)
app.register_blueprint(quotes_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(payments_bp)
app.register_blueprint(photos_bp)
app.register_blueprint(user_interactions_bp)
app.register_blueprint(compatibility_bp)
app.register_blueprint(forecasts_bp)
app.register_blueprint(nlp_queries_bp)
app.register_blueprint(ai_models_bp)
app.register_blueprint(inventory_bp)

# Run the application
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
