#!/usr/bin/python3
"""
Module to handle RESTFul api actions for User objects
Methods:GET, POST, PUT and DELETE
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def users_all():
    """Gets all User objects from storage"""
    my_list = []
    objs_dict = storage.all(User)
    for item in objs_dict.values():
        obj_to_dict = item.to_dict()
        my_list.append(obj_to_dict)
    return (jsonify(my_list))

@app_views.route('/users/<user_id>', methods=['GET'])
def find_user(user_id):
    """Finds a User based on the ID passed"""
    obj = storage.get(User, user_id)

    if obj:
        return (jsonify({obj.to_dict()}))
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User based on the ID passed"""
    obj = storage.get(User, user_id)

    if obj:
        storage.delete(obj)
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/users', methods=['POST'])
def post_user():
    """Makes a post request"""
    if not request.is_json:
        return (jsonify('Not a JSON'), 400)
    data = request.get_json()
    if not (data.get('email')):
        return (jsonify('Missing email'), 400)
    if not (data.get('password')):
        return (jsonify('Missing password'), 400)
    obj = User(**data)
    storage.new(obj)
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def alter_user(user_id):
    """alters a User based on the ID passed"""
    if not request.is_json:
        return jsonify({'Not a JSON'}), 400

    data = request.get_json()

    if not (data.get('name')):
        return (jsonify('Missing name'), 400)
    obj = storage.get(User, user_id)

    if obj:
        lst = ['id', 'updated_at', 'created_at', 'email']
        for key in lst:
            if data.get(key):
                del data[key]
        for key, value in data.items():
            setattr(obj, key, value)
        storage.save()
        return (jsonify(obj.to_dict()), 200)
    else:
        abort(404)
