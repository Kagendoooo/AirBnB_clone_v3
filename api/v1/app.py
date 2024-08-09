#!/usr/bin/python3
"""
This module defines the main Flask application for the API.
"""

from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """
    Closes the storage on teardown.
    """
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """JSON 404 erro"""
    res = jsonify({"error": "Not found"})
    res.status_code = 404
    return res


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
