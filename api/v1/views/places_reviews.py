#!/usr/bin/python3
"""
New view for Review object
Handles all default RESTFul API actions
"""
from flask import Blueprint, jsonify, request, abort, make_response
from models import storage
from models.place import Place
from models.review import Review
from models.user import User

app_views = Blueprint('app_views', __name__)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a Review object by review_id
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404, description="Review not found")
    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object by review_id
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404, description="Review not found")
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """
    Creates a new Review object for a given place_id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404, description="Place not found")

    if not request.is_json:
        abort(400, description="Not a JSON")

    req_data = request.get_json()

    if 'user_id' not in req_data:
        abort(400, description="Missing user_id")
    if 'text' not in req_data:
        abort(400, description="Missing text")

    user = storage.get(User, req_data['user_id'])
    if not user:
        abort(404, description="User not found")

    req_data['place_id'] = place_id
    review = Review(**req_data)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Updates a Review object by review_id
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404, description="Review not found")

    if not request.is_json:
        abort(400, description="Not a JSON")

    req_data = request.get_json()

    for key, value in req_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200
