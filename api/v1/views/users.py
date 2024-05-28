#!/usr/bin/python3
"""
Module to handle RESTFul api actions for User objects
Methods:GET, POST, PUT and DELETE
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def users_all():
    """Gets all User objects from storage"""
    my_list = []
    objs_dict = storage.all(User)
    for item in objs_dict.values():
        obj_to_dict = item.to_dict()
        my_list.append(obj_to_dict)
    return jsonify(my_list), 200


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def find_user(user_id):
    """Finds a User based on the ID passed"""
    obj = storage.get(User, user_id)

    if obj:
        return jsonify(obj.to_dict()), 200
    else:
        abort(404)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User based on the ID passed"""
    obj = storage.get(User, user_id)

    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def post_user():
    """Makes a post request"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if not (data.get('email')):
        abort(400, 'Missing email')
    if not (data.get('password')):
        abort(400, 'Missing password')
    obj = User(**data)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def alter_user(user_id):
    """alters a User based on the ID passed"""
    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()

    if not (data.get('name')):
        abort(400, 'Missing name')
    obj = storage.get(User, user_id)

    if obj:
        lst = ['id', 'updated_at', 'created_at', 'email']
        for key in lst:
            if data.get(key):
                del data[key]
        for key, value in data.items():
            setattr(obj, key, value)
        storage.save()
        return jsonify(obj.to_dict()), 200
    else:
        abort(404)
