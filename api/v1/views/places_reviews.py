#!/usr/bin/python3
"""
New view for Review object
Handles all default RESTFul API actions
"""

from models.place import Place
from models.user import User
from models.review import Review
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/place_review/get_place_reviews.yml', methods=['GET'])
def get_place_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404, description="Place not found")

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/places/<place_id>/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/place_review/delete_place_review.yml',
           methods=['DELETE'])
def delete_place_review(place_id, review_id):
    """
    Deletes a Review object from a Place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404, description="Place not found")

    review = storage.get(Review, review_id)
    if not review:
        abort(404, description="Review not found")

    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/place_review/post_place_review.yml',
           methods=['POST'])
def create_review(place_id):
    """
    Creates a new Review for a Place
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
@swag_from('documentation/reviews/put_reviews.yml', methods=['PUT'])
def update_review(review_id):
    """
    Updates a Review
    """
    review_instance = storage.get(Review, review_id)
    if not review_instance:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(review_instance, key, value)

    storage.save()
    return jsonify(review_instance.to_dict()), 200

