"""
API routes for Virtual Dealer
"""

from flask import Flask, jsonify
import store

app = Flask(__name__)


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
    response = store.add_new_player_to_game(game_id)
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


@app.route("/")
def root():
    """
    Main application
    """
    return jsonify(message="Hello"), 200


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.

    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)
