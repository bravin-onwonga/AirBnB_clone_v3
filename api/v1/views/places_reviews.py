#!/usr/bin/python3
"""
Handles all default RESTFul API actions for Review class
Methods:GET, POST, PUT and DELETE
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.place import Place
from models import storage
from models.review import Review
from models.user import User


@app_views.route('places/<place_id>/reviews', methods=['GET'])
def all_reviews(place_id):
    """Lists all reviews tied to place"""
    place = storage.get(Place, place_id)

    if place:
        my_list = []
        reviews = storage.all(Review)
        for review in reviews.values():
            obj_dict = review.to_dict()
            if (obj_dict.get('place_id') == place_id):
                my_list.append(obj_dict)
        return (jsonify({my_list}))
    else:
        abort(404)


@app_views.route('reviews/<review_id>', methods=['GET'])
def find_review(review_id):
    """Find a review based on ID passed"""
    review = storage.get(Review, review_id)

    if review:
        return (review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Deletes a review based on the ID passed"""
    obj = storage.get(Review, review_id)

    if obj:
        storage.delete(obj)
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def post_review(place_id):
    """Makes a post request"""
    if not request.is_json:
        return (jsonify('Not a JSON'), 400)
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return (jsonify('Missing user_id'), 400)
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    obj = Review(**data)
    storage.new(obj)
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def alter_review(review_id):
    """alters a review based on the ID passed"""
    if not request.is_json:
        return jsonify({'Not a JSON'}), 400

    data = request.get_json()

    obj = storage.get(Review, review_id)

    if obj:
        lst = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key in lst:
            if data.get(key):
                del data[key]
        for key, value in data.items():
            setattr(obj, key, value)
        storage.save()
        return (jsonify(obj.to_dict()), 200)
    else:
        abort(404)
