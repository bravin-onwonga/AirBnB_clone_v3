#!/usr/bin/python3
"""
Creates a new view for the link between Place objects and
Amenity objects that handles all default RESTFul API actions
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
import models
from models.place import Place

@app_views.route('places/<place_id>/amenities',
                 strict_false=False, methods=['GET'])
def all_Place_amenities(place_id):
    """Lists all amenities linked to a place"""
    place = storage.get(Place, place_id)

    if place:
        my_list = []

        if (models.storage_t == 'db'):
            pass
        pass
    else:
        abort(404)
