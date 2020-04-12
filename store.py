"""
Wrapper around datastore
"""
import datetime
from google.cloud import datastore
import cards


class Store:
    """
    Class wrappiong datastore
    """

    def __init__(self):
        """
        Initialize store class
        """
        self.ds_client = datastore.Client()

    def create_new_game(self):
        """
        Create a new game
        """
        entity = datastore.Entity(key=self.ds_client.key("Game"))
        entity.update(
            {
                "timestamp_created": datetime.datetime.now(),
                "timestamp_updated": datetime.datetime.now(),
                "state": "NOT_STARTED",
                "decks": {"stock": [], "discard_pile": []},
            }
        )
        self.ds_client.put(entity)

        return {"game_id": entity.key.id}

    def get_game(self, game_id):
        """
        Get info about a game
        """
        key = self.ds_client.key("Game", game_id)
        entity = self.ds_client.get(key)

        return entity

    def list_games(self, count):
        """
        Get a list of the most recent games
        """
        query = self.ds_client.query(kind="Game")
        query.order = ["-timestamp_updated"]
        games = list(query.fetch(limit=count))

        # add game_id into dict
        response = []
        for game in games:
            game["game_id"] = game.key.id
            response.append(game)
        return response

    def add_new_player_to_game(self, game_id, name, email):
        """
        Add a new player to a game
        """
        game_key = self.ds_client.key("Game", game_id)
        player_key = self.ds_client.key("Player", parent=game_key)
        entity = datastore.Entity(key=player_key)
        entity.update(
            {
                "name": name,
                "email": email,
                "timestamp_created": datetime.datetime.now(),
                "timestamp_updated": datetime.datetime.now(),
                "decks": {"hand": [], "discard_pile": []},
            }
        )
        self.ds_client.put(entity)

        return {"game_id": game_id, "player_id": entity.key.id}

    def get_player(self, game_id, player_id):
        """
        Get info about a player in a game
        """
        game_key = self.ds_client.key("Game", game_id)
        player_key = self.ds_client.key("Player", player_id, parent=game_key)
        entity = self.ds_client.get(player_key)
        return entity

    def list_players(self, game_id):
        """
        Get a list of players in a game
        """
        query = self.ds_client.query(kind="Player")
        query.ancestor = self.ds_client.key("Game", game_id)
        players = list(query.fetch())

        # add player_id into dict
        response = []
        for player in players:
            player["player_id"] = player.key.id
            response.append(player)
        return response

    def add_new_deck_to_game(self, game_id, deck_name):
        """
        Add a new deck to a game
        """
        with self.ds_client.transaction():
            key = self.ds_client.key("Game", game_id)
            game = self.ds_client.get(key)

            if deck_name in game["decks"]:
                return None

            game["decks"].update({f"{deck_name}": []})

            self.ds_client.put(game)

        return game
