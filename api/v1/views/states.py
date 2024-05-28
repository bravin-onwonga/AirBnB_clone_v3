#!/usr/bin/python3
"""
Module to handle RESTFul api actions for state objects
Methods:GET, POST, PUT and DELETE
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def all_states():
    """Gets all state objects from storage"""
    my_list = []
    objs_dict = storage.all(State)
    for item in objs_dict.values():
        obj_to_dict = item.to_dict()
        my_list.append(obj_to_dict)
    return jsonify(my_list), 200


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def find_state(state_id):
    """Finds a state based on the ID passed"""
    obj = storage.get(State, state_id)

    if obj:
        return jsonify(obj.to_dict()), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """Deletes a state based on the ID passed"""
    obj = storage.get(State, state_id)

    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post_state():
    """Makes a post request"""
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')
    obj = State(**data)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def alter_state(state_id):
    """alters a state based on the ID passed"""
    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()

    obj = storage.get(State, state_id)

    if obj:
        lst = ['id', 'updated_at', 'created_at']
        for key, value in data.items():
            if key not in lst:
                setattr(obj, key, value)
        storage.save()
        return jsonify(obj.to_dict()), 200
    else:
        abort(404)
