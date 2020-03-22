"""
API routes for Virtual Dealer
"""

from flask import Flask

app = Flask(__name__)


@app.route("/api/game/new", methods=["POST"])
def new_game():
    """
    Create a new game
    """
    return "new game"


@app.route("/api/game/<int:game_id>")
def game_info(game_id):
    """
    Get Game Info by game_id
    """
    return f"game id: {game_id}"


@app.route("/api/game/list/<int:count>")
@app.route("/api/game/list")
def game_list(count=10):
    """
    List Games by recent
    """
    return f"game count {count}"


@app.route("/api/game/<int:game_id>/player/new", methods=["POST"])
def new_player(game_id):
    """
    Add a new player to a game
    """
    return f"new player for game od {game_id}"


@app.route("/api/game/<int:game_id>/player/<int:player_id>")
def player_info(game_id, player_id):
    """
    Get player info by game_id and player_id
    """
    return f"game id: {game_id}, player_id: {player_id}"


@app.route("/")
def root():
    """
    Main application
    """
    return "Hello"


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.

    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)
