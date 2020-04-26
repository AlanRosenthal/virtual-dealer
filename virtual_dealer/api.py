"""
APIs for webapp
"""

from flask import Flask, jsonify, request
from jsonschema import validate, SchemaError, ValidationError
import virtual_dealer.store
from virtual_dealer.exceptions import InvalidMove

app = Flask("VirtualDealer")
store = virtual_dealer.store.Store()


@app.route("/api/game/new", methods=["POST"])
def new_game():
    """
    Create a new game
    """
    response = store.create_new_game()
    return jsonify(response), 201


@app.route("/api/game/<int:game_id>", methods=["GET"])
def game_info(game_id):
    """
    Get Game Info by game_id
    """
    response = store.get_game(game_id)
    return jsonify(response), 200


@app.route("/api/game/list/<int:count>", methods=["GET"])
@app.route("/api/game/list")
def game_list(count=10):
    """
    List Games by recent
    """
    response = store.list_games(count)
    return jsonify(response), 200


@app.route("/api/game/<int:game_id>/player/new", methods=["POST"])
def new_player(game_id):
    """
    Add a new player to a game
    """
    if not request.is_json:
        return 400

    data = request.get_json()
    if "email" not in data or "name" not in data:
        return 400

    response = store.add_new_player_to_game(game_id, data["name"], data["email"])
    return jsonify(response), 201


@app.route("/api/game/<int:game_id>/player/list", methods=["GET"])
def player_list(game_id):
    """
    List all players added to a specific game
    """
    response = store.list_players(game_id)
    return jsonify(response), 200


@app.route("/api/game/<int:game_id>/player/<int:player_id>", methods=["GET"])
def player_info(game_id, player_id):
    """
    Get player info by game_id and player_id
    """
    response = store.get_player(game_id, player_id)
    return jsonify(response), 200


@app.route("/api/game/<int:game_id>/deck/new", methods=["POST"])
def game_deck_new(game_id):
    """
    Add a new deck to the game
    """
    if not request.is_json:
        error = {"error": "Request data must be json"}
        return jsonify(error), 400

    data = request.get_json()

    schema = {
        "type": "object",
        "properties": {"name": {"type": "string",}, "is_full": {"type": "boolean"}},
        "required": ["name"],
    }
    try:
        validate(instance=data, schema=schema)
    except SchemaError as schema_error:
        error = {"error": f"Schema error: {schema_error}"}
        return jsonify(error), 500
    except ValidationError as validation_error:
        error = {"error": f"Schema validation failed: {validation_error}"}
        return jsonify(error), 400

    is_full = False
    if "is_full" in data:
        is_full = data["is_full"]

    response = store.add_new_deck_to_game(game_id, data["name"], is_full)
    return jsonify(response), 201


@app.route("/api/game/<int:game_id>/deck/list", methods=["GET"])
def game_deck_list(game_id):
    """
    List all game decks
    """
    response = store.list_game_decks(game_id)
    return jsonify(response), 200


@app.route("/api/game/<int:game_id>/player/<int:player_id>/deck/new", methods=["POST"])
def player_deck_new(game_id, player_id):
    """
    Add a new deck to a player
    """
    if not request.is_json:
        error = {"error": "Request data must be json"}
        return jsonify(error), 400

    data = request.get_json()
    if "name" not in data:
        error = {"error": "Key 'name' expected in response data"}
        return jsonify(error), 400

    response = store.add_new_deck_to_player(game_id, player_id, data["name"])
    return jsonify(response), 201


@app.route("/api/game/<int:game_id>/player/<int:player_id>/deck/list", methods=["GET"])
def player_deck_list(game_id, player_id):
    """
    List all player decks
    """
    response = store.list_player_decks(game_id, player_id)
    return jsonify(response), 200


@app.route("/api/game/<int:game_id>/card/move", methods=["POST"])
def deck_move(game_id):
    """
    Move cards from one deck to another desk
    """
    if not request.is_json:
        error = {"error": "Request data must be json"}
        return jsonify(error), 400

    data = request.get_json()
    schema = {
        "type": "object",
        "properties": {
            "cards": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "rank": {"type": "string"},
                        "suit": {"type": "string"},
                    },
                    "required": ["rank", "suit"],
                },
            },
            "source": {
                "type": "object",
                "properties": {
                    "player_id": {"type": "number"},
                    "deck_id": {"type": "number"},
                },
                "required": ["deck_id"],
            },
            "destination": {
                "type": "object",
                "properties": {
                    "player_id": {"type": "number"},
                    "deck_id": {"type": "number"},
                },
                "required": ["deck_id"],
            },
        },
        "required": ["cards", "source", "destination"],
    }
    try:
        validate(instance=data, schema=schema)
    except SchemaError as schema_error:
        error = {"error": f"Schema error: {schema_error}"}
        return jsonify(error), 500
    except ValidationError as validation_error:
        error = {"error": f"Schema validation failed: {validation_error}"}
        return jsonify(error), 400

    try:
        store.cards_move(game_id, data["source"], data["destination"], data["cards"])
    except InvalidMove as invalid_move:
        error = {"error": f"Error moving card: {invalid_move}"}
        return jsonify(error), 400
    return "", 204


@app.route("/")
def root():
    """
    Main application
    """
    return jsonify(message="Hello"), 200
