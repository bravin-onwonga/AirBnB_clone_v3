#!/usr/bin/python3

from flask import Blueprint, Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

app = app_views

@app.teardown_appcontext
def close():
    storage.close()

if __name__ == "__main__":
    my_host = getenv('HBNB_API_HOST')
    if not(my_host):
        my_host = 'localhost'

    my_port = getenv('HBNB_API_PORT')
    if not (my_port):
        my_port = 5000

    app.views.run(host=my_host, port=my_port, threaded=True)
