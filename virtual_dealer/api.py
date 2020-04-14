"""
APIs for webapp
"""

from flask import Flask, jsonify, request
import virtual_dealer.store

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
def new_deck_to_game(game_id):
    """
    Add a new deck to the game
    """
    if not request.is_json:
        error = {"error": "Request data must be json"}
        return jsonify(error), 400

    data = request.get_json()
    if "name" not in data:
        error = {"error": "Key 'name' expected in response data"}
        return jsonify(error), 400

    response = store.add_new_deck_to_game(game_id, data["name"])
    if not response:
        error = {"error": f"unable to add new deck: {data['name']}"}
        return jsonify(error), 400
    return jsonify(response), 201


@app.route("/")
def root():
    """
    Main application
    """
    return jsonify(message="Hello"), 200
