#!/usr/bin/python3
"""Module to handle RESTFul api actions"""

from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """Simple route that prints an custom response"""
    return (jsonify({'status': 'OK'}))


@app_views.route('/stats', methods=['GET'])
def stats():
    """Calls the count method in storage for all classes"""
    my_dict = {}
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}

    for key, value in classes.items():
        count = storage.count(value)
        my_dict[key] = count
    return (jsonify(my_dict))
