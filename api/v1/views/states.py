#!/usr/bin/python3
"""
Module to handle RESTFul api actions for state objects
Methods:GET, POST, PUT and DELETE
"""

from flask import abort, jsonify, request
import json
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def all():
    """Gets all state objects from storage"""
    my_list = []
    objs_dict = storage.all(State)
    for item in objs_dict.values():
        obj_to_dict = item.to_dict()
        my_list.append(obj_to_dict)
    return (jsonify(my_list))


@app_views.route('/states/<state_id>', methods=['GET'])
def find_state(state_id):
    """Finds a state based on the ID passed"""
    objs_dict = storage.all(State)
    key = 'State.{}'.format(state_id)
    obj = objs_dict.get(key)

    if obj:
        return (obj.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a state based on the ID passed"""
    objs_dict = storage.all(State)
    key = 'State.{}'.format(state_id)
    obj = objs_dict.get(key)

    if obj:
        storage.delete(obj)
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states', methods=['POST'])
def post_state():
    """Makes a post request"""
    if not request.is_json:
        return (jsonify('Not a JSON'), 400)
    data = request.get_json()
    if not (data.get('name')):
        return (jsonify('Missing name'), 400)
    obj = State(**data)
    storage.new(obj)
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def alter_state(state_id):
    """alters a state based on the ID passed"""
    if not request.is_json:
        return jsonify({'Not a JSON'}), 400

    data = request.get_json()
    print(type(data))
    if not (data.get('name')):
        return (jsonify('Missing name'), 400)
    obj = storage.get(State, state_id)

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
