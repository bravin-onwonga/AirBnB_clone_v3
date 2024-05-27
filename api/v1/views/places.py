#!/usr/bin/python3
"""
Module to handle RESTFul api actions for Place objects
Methods:GET, POST, PUT and DELETE
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def places_all(city_id):
    """Gets all Place objects from storage"""
    my_list = []
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    objs_dict = storage.all(Place)
    for item in objs_dict.values():
        obj_to_dict = item.to_dict()
        if (obj_to_dict.get('city_id') == city_id):
            my_list.append(obj_to_dict)
    return (jsonify(my_list))


@app_views.route('/places/<place_id>', methods=['GET'])
def find_place(place_id):
    """Finds a Place object based on the ID passed"""
    obj = storage.get(Place, place_id)

    if obj:
        return (jsonify({obj.to_dict()}))
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_Place(place_id):
    """Deletes a Place based on the ID passed"""
    obj = storage.get(Place, place_id)

    if obj:
        storage.delete(obj)
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def post_place(city_id):
    """Makes a post request"""
    if not request.is_json:
        return (jsonify('Not a JSON'), 400)
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return (jsonify('Missing user_id'), 400)
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    obj = Place(**data)
    storage.new(obj)
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def alter_Place(place_id):
    """alters a Place based on the ID passed"""
    if not request.is_json:
        return jsonify({'Not a JSON'}), 400

    data = request.get_json()

    if not (data.get('name')):
        return (jsonify('Missing name'), 400)
    obj = storage.get(Place, place_id)

    if obj:
        lst = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key in lst:
            if data.get(key):
                del data[key]
        for key, value in data.items():
            setattr(obj, key, value)
        storage.save()
        return (jsonify(obj.to_dict()), 200)
    else:
        abort(404)
