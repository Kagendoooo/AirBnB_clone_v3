#!/usr/bin/python3
'''Contains the cities view for the API.'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_cities(state_id=None, city_id=None):
    if request.method == 'GET':
        if state_id:
            return get_cities_by_state(state_id)
        if city_id:
            return get_city(city_id)
        raise MethodNotAllowed(['GET'])
    if request.method == 'POST' and state_id:
        return create_city(state_id)
    if request.method == 'DELETE' and city_id:
        return delete_city(city_id)
    if request.method == 'PUT' and city_id:
        return update_city(city_id)
    raise MethodNotAllowed(['GET', 'POST', 'DELETE', 'PUT'])


def get_cities_by_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        raise NotFound(description="State not found")
    return jsonify([city.to_dict() for city in state.cities])


def get_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        raise NotFound(description="City not found")
    return jsonify(city.to_dict())


def create_city(state_id):
    state = storage.get(State, state_id)
    if not state:
        raise NotFound(description="State not found")

    data = request.get_json()
    if not isinstance(data, dict):
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


def delete_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        raise NotFound(description="City not found")
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


def update_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        raise NotFound(description="City not found")
    data = request.get_json()
    if not isinstance(data, dict):
        raise BadRequest(description='Not a JSON')
    for key, value in data.items():
        if key not in {'id', 'state_id', 'created_at', 'updated_at'}:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
