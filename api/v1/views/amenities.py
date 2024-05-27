#!/usr/bin/python3
"""
Module to handle RESTFul api actions for Amenity objects
Methods:GET, POST, PUT and DELETE
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def amenities_all():
    """Gets all Amenity objects from storage"""
    my_list = []
    objs_dict = storage.all(Amenity)
    for item in objs_dict.values():
        obj_to_dict = item.to_dict()
        my_list.append(obj_to_dict)
    return (jsonify(my_list))


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def find_amenity(amenity_id):
    """Finds a Amenity based on the ID passed"""
    obj = storage.get(Amenity, amenity_id)

    if obj:
        return (obj.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes a Amenity based on the ID passed"""
    obj = storage.get(Amenity, amenity_id)

    if obj:
        storage.delete(obj)
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'])
def post_amenity():
    """Makes a post request"""
    if not request.is_json:
        return (jsonify('Not a JSON'), 400)
    data = request.get_json()
    if not (data.get('name')):
        return (jsonify('Missing name'), 400)
    obj = Amenity(**data)
    storage.new(obj)
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def alter_amenity(amenity_id):
    """alters a Amenity based on the ID passed"""
    if not request.is_json:
        return jsonify({'Not a JSON'}), 400

    data = request.get_json()

    if not (data.get('name')):
        return (jsonify('Missing name'), 400)
    obj = storage.get(Amenity, amenity_id)

    if obj:
        lst = ['id', 'updated_at', 'created_at']
        for key in lst:
            if data.get(key):
                del data[key]
        for key, value in data.items():
            setattr(obj, key, value)
        storage.save()
        return (jsonify(obj.to_dict()), 200)
    else:
        abort(404)
