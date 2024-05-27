#!/usr/bin/python3
"""
Module to handle RESTFul api actions
Registers the blueprint to app_views which contains our url_prefix
Our api run on localhost port 5000
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)

app.register_blueprint(app_views)
app.url_map.strict_slashes = False

CORS(app, resources={r"app/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def close(exception):
    """Calls the close method based on the storage"""
    storage.close()


@app.errorhandler(404)
def handle_404_error(ex):
    """Handles the page not found(404) error"""
    return (jsonify({"error": "Not found"}))


if __name__ == "__main__":
    my_host = getenv('HBNB_API_HOST')
    if not (my_host):
        my_host = '0.0.0.0'

    my_port = getenv('HBNB_API_PORT')
    if not (my_port):
        my_port = 5000

    app.run(host=my_host, port=my_port, threaded=True, debug=True)
