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


def get_games(count):
    """
    Get a list of the most recent games
    """
    response = []
    for game_id in range(count):
        response.append(
            {
                "game_id": 1000 + game_id,
                "timestamp_created": 6,
                "timestamp_updated": 43,
                "state": "NOT_STARTED",
            }
        )
    return response


def add_new_player_to_game(game_id):
    """
    Add a new player to a game
    """
    return {"game_id": game_id, "player_id": 435}


def get_player(game_id, player_id):
    """
    Get info about a game
    """
    return {
        "game_id": game_id,
        "player_id": player_id,
        "name": "Alan",
        "email": "alan.rosenthal@gmail.com",
        "timestamp_created": 1,
        "timestamp_updated": 2,
    }
