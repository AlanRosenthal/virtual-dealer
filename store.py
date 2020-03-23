"""
Wrapper around datastore
"""


def create_new_game():
    """
    Create a new game
    """
    return {"game_id": 1234}


def get_game(game_id):
    """
    Get info about a game
    """
    return {
        "game_id": game_id,
        "timestamp_created": 1,
        "timestamp_updated": 2,
        "state": "NOT_STARTED",
    }


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
