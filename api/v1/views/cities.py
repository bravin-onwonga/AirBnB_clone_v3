#!/usr/bin/python3
"""
Module to handle RESTFul api actions for City objects
Methods:GET, POST, PUT and DELETE
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def city_all(state_id):
    """Gets all City objects from storage"""
    my_list = []
    state = storage.get(State, state_id)
    if not (state):
        abort(404)
    objs_dict = storage.all(City)
    for item in objs_dict.values():
        obj_to_dict = item.to_dict()
        if (obj_to_dict.get('state_id') == state_id):
            my_list.append(obj_to_dict)
    return (jsonify(my_list))


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['GET'])
def find_city(city_id):
    """Finds a City based on the ID passed"""
    objs_dict = storage.all(City)
    key = 'City.{}'.format(city_id)
    obj = objs_dict.get(key)

    if obj:
        return (obj.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City based on the ID passed"""
    objs_dict = storage.all(City)
    key = 'City.{}'.format(city_id)
    obj = objs_dict.get(key)

    if obj:
        storage.delete(obj)
        storage.save()
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def post_city(state_id):
    """Makes a post request"""
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    state = storage.get(State, state_id)
    if not (state):
        abort(404)
    if not (data.get('name')):
        abort(400, 'Missing name')
    obj = City(**data)
    storage.new(obj)
    storage.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['PUT'])
def alter_city(city_id):
    """alters a City based on the ID passed"""
    if not request.is_json:
        return jsonify({'Not a JSON'}), 400

    data = request.get_json()

    obj = storage.get(City, city_id)

    if obj:
        lst = ['id', 'updated_at', 'created_at', 'state_id']
        for key in lst:
            if data.get(key):
                del data[key]
        for key, value in data.items():
            setattr(obj, key, value)
        storage.save()
        return (jsonify(obj.to_dict()), 200)
    else:
        abort(404)
