#!/usr/bin/python3
"""
REstful API for states
"""
from flask import jsonify, request, make_response, abort
from flasgger.utils import swag_from
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_state.yml', methods=['GET'])
def get_states():
    """Retrieve the list of all States"""
    all_states = storage.all(State).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_id_state.yml', methods=['get'])
def get_state(state_id):
    """ get a state """
    state_instance = storage.get(State, state_id)
    if not state_instance:
        abort(404)
    return jsonify(state_instance.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/state/delete_state.yml', methods=['DELETE'])
def delete_state(state_id):
    """Delete a State """

    state_instance = storage.get(State, state_id)

    if not state_instance:
        abort(404)

    storage.delete(state_instance)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
@swag_from('documentation/state/post_state.yml', methods=['POST'])
def create_state():
    """Creates a State"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    new_state = State(**data)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/state/update_state.yml', methods=['PUT'])
def update_state(state_id):
    """Update state"""
    state_instance = storage.get(State, state_id)

    if not state_instance:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state_instance, key, value)
    storage.save()
    return make_response(jsonify(state_instance.to_dict()), 200)
