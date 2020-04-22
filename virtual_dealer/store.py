"""
Wrapper around datastore
"""
import datetime
from google.cloud import datastore
import virtual_dealer.cards


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
        game_key = self.ds_client.key("Game")
        game = datastore.Entity(key=game_key)
        game.update(
            {
                "timestamp_created": datetime.datetime.now(),
                "timestamp_updated": datetime.datetime.now(),
            }
        )

        self.ds_client.put(game)
        self.add_new_deck_to_game(
            game.key.id, "stock", virtual_dealer.cards.create_full_deck()
        )

        return {"game_id": game.key.id}

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

    def add_new_deck_to_game(self, game_id, deck_name, cards=None):
        """
        Add a new deck to a game
        """
        if not cards:
            cards = []
        game_key = self.ds_client.key("Game", game_id)
        deck_key = self.ds_client.key("Deck", parent=game_key)
        deck = datastore.Entity(key=deck_key)
        deck.update(
            {
                "name": deck_name,
                "cards": cards,
                # "timestamp_created": datetime.datetime.now(),
                # "timestamp_updated": datetime.datetime.now(),
            }
        )
        self.ds_client.put(deck)

        return {"game_id": game_id, "deck_id": deck.key.id}

    def list_game_decks(self, game_id):
        """
        Get a list of game decks
        """
        query = self.ds_client.query(kind="Deck")
        query.ancestor = self.ds_client.key("Game", game_id)
        decks = list(query.fetch())

        # add player_id into dict
        response = []
        for deck in decks:
            deck["deck_id"] = deck.key.id
            response.append(deck)
        return response

    def add_new_deck_to_player(self, game_id, player_id, deck_name):
        """
        Add a new deck to a player
        """
        player_key = self.ds_client.key("Player", player_id)
        deck_key = self.ds_client.key("Deck", parent=player_key)
        deck = datastore.Entity(key=deck_key)
        deck.update(
            {
                "name": deck_name,
                "cards": [],
                # "timestamp_created": datetime.datetime.now(),
                # "timestamp_updated": datetime.datetime.now(),
            }
        )
        self.ds_client.put(deck)

        return {"game_id": game_id, "player_id": player_id, "deck_id": deck.key.id}

    def list_player_decks(self, game_id, player_id):
        """
        Get a list of game decks
        """
        game_key = self.ds_client.key("Game", game_id)
        player_key = self.ds_client.key("Player", player_id, ancestor=game_key)
        query = self.ds_client.query(kind="Deck")
        query.ancestor = player_key
        decks = list(query.fetch())

        # add player_id into dict
        response = []
        for deck in decks:
            deck["deck_id"] = deck.key.id
            response.append(deck)
        return response

    def cards_move(self, game_id, src, dest, cards):
        """
        Move cards from src desk to dest decks
        """
        print(dest)
        with self.ds_client.transaction():
            game_key = self.ds_client.key("Game", game_id)
            if "player_id" in src:
                # unsure why, but if `parent=game_key` is added to `player_key`, get() returns None
                player_key = self.ds_client.key("Player", src["player_id"])
                src_deck_key = self.ds_client.key(
                    "Deck", src["deck_id"], parent=player_key
                )
            else:
                src_deck_key = self.ds_client.key(
                    "Deck", src["deck_id"], parent=game_key
                )
            src_deck = self.ds_client.get(src_deck_key)

            if "player_id" in dest:
                # unsure why, but if `parent=game_key` is added to `player_key`, get() returns None
                player_key = self.ds_client.key("Player", dest["player_id"])
                dest_deck_key = self.ds_client.key(
                    "Deck", dest["deck_id"], parent=player_key
                )
            else:
                dest_deck_key = self.ds_client.key(
                    "Deck", dest["deck_id"], parent=game_key
                )
            dest_deck = self.ds_client.get(dest_deck_key)

            for card in cards:
                if card not in src_deck["cards"]:
                    raise Exception(f"Card: {card} not in deck: {src_deck.key.id}")
                src_deck["cards"].remove(card)
                dest_deck["cards"].append(card)

            self.ds_client.put(src_deck)
            self.ds_client.put(dest_deck)
