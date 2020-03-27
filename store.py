"""
Wrapper around datastore
"""
import datetime
from google.cloud import datastore

datastore_client = datastore.Client()


def create_new_game():
    """
    Create a new game
    """
    entity = datastore.Entity(key=datastore_client.key("Game"))
    entity.update(
        {
            "timestamp_created": datetime.datetime.now(),
            "timestamp_updated": datetime.datetime.now(),
            "state": "NOT_STARTED",
        }
    )
    datastore_client.put(entity)

    return {"game_id": entity.key.id}


def get_game(game_id):
    """
    Get info about a game
    """
    key = datastore_client.key("Game", game_id)
    entity = datastore_client.get(key)

    return entity


def list_games(count):
    """
    Get a list of the most recent games
    """
    query = datastore_client.query(kind="Game")
    query.order = ["-timestamp_updated"]
    games = list(query.fetch(limit=count))

    # add game_id into dict
    response = []
    for game in games:
        game["game_id"] = game.key.id
        response.append(game)
    return response


def add_new_player_to_game(game_id, name, email):
    """
    Add a new player to a game
    """
    game_key = datastore_client.key("Game", game_id)
    player_key = datastore_client.key("Player", parent=game_key)
    entity = datastore.Entity(key=player_key)
    entity.update(
        {
            "name": name,
            "email": email,
            "timestamp_created": datetime.datetime.now(),
            "timestamp_updated": datetime.datetime.now(),
        }
    )
    datastore_client.put(entity)

    return {"game_id": game_id, "player_id": entity.key.id}


def get_player(game_id, player_id):
    """
    Get info about a player in a game
    """
    game_key = datastore_client.key("Game", game_id)
    player_key = datastore_client.key("Player", player_id, parent=game_key)
    entity = datastore_client.get(player_key)
    return entity


def list_players(game_id):
    """
    Get a list of players in a game
    """
    query = datastore_client.query(kind="Player")
    query.ancestor = datastore_client.key("Game", game_id)
    players = list(query.fetch())

    # add game_id into dict
    response = []
    for player in players:
        player["player_id"] = player.key.id
        response.append(player)
    return response
