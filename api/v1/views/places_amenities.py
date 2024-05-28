#!/usr/bin/python3
"""
Creates a new view for the link between Place objects and
Amenity objects that handles all default RESTFul API actions
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
import models
from models.amenity import Amenity
from models.place import Place


@app_views.route('places/<place_id>/amenities',
                 strict_slashes=False, methods=['GET'])
def all_place_amenities(place_id):
    """Lists all amenities linked to a place"""
    place = storage.get(Place, place_id)

    if place:
        my_list = []

        if (models.storage_t == 'db'):
            for item in place.amenities:
                my_list.append(item.to_dict())
        else:
            amenity_ids_lst = place.amenity_ids
            for id in amenity_ids_lst:
                obj = storage.get(Amenity, id)
                my_list.append(obj.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """Deletes an amenity based on the ID passed"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if (models.storage_t != 'db'):
        if amenity_id not in place.amenity_ids:
            abort(404)
        else:
            place.amenity_ids.remove(amenity_id)
            storage.save()
            return jsonify({}), 200
    elif (models.storage_t == 'db'):
        if amenity not in place.amenities:
            abort(404)
        else:
            place.amenities.remove(amenity)
            storage.save()
            return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def add_place_amenity(place_id, amenity_id):
    """Adds an amenity to a place"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if (models.storage_t != 'db'):
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenity_ids.append(amenity_id)
            storage.save()
            return jsonify(amenity.to_dict()), 201
    elif (models.storage_t == 'db'):
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenities.append(amenity)
            storage.save()
            return jsonify(amenity.to_dict()), 201
