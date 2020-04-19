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
        entity = datastore.Entity(key=self.ds_client.key("Game"))
        entity.update(
            {
                "timestamp_created": datetime.datetime.now(),
                "timestamp_updated": datetime.datetime.now(),
                "state": "NOT_STARTED",
                "decks": {
                    "stock": virtual_dealer.cards.create_full_deck(),
                    "discard_pile": [],
                },
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

    # pylint: disable=too-many-arguments
    # pylint: disable=bad-continuation
    # black and pylint disagree with each on this, see https://github.com/PyCQA/pylint/issues/741
    def move_cards_game_to_all_players(
        self, game_id, game_deck_name, player_deck_name, card_count
    ):
        """
        Deal cards to all players
        """
        with self.ds_client.transaction():
            key = self.ds_client.key("Game", game_id)
            game = self.ds_client.get(key)

            query = self.ds_client.query(kind="Player")
            query.ancestor = self.ds_client.key("Game", game_id)
            players = list(query.fetch())

            if game_deck_name not in game["decks"]:
                raise Exception(f"Game deck not found: {game_deck_name}")

            for player in players:
                # copy game's deck so we don't run into issues when we modify it
                game_deck = game["decks"][game_deck_name].copy()

                if player_deck_name not in player["decks"]:
                    raise Exception(
                        f"Player {player.key.id} deck not found: {player_deck_name}"
                    )

                if len(game_deck) < card_count:
                    raise Exception(
                        f"Not enough cards in game's deck: {game_deck_name}"
                    )

                # move card_count cards from game_deck_name to player_deck_name
                game["decks"][game_deck_name] = game_deck[card_count:]
                player["decks"][player_deck_name].extend(game_deck[:card_count])

                # save player entity
                player["timestamp_updated"]: datetime.datetime.now()
                self.ds_client.put(player)

            # save game entity
            game["timestamp_updated"]: datetime.datetime.now()
            self.ds_client.put(game)

    def move_card_player(self, game_id, player_id, source_deck, destination_deck, card):
        """
        Move cards between a player's desk
        """
        with self.ds_client.transaction():

            game_key = self.ds_client.key("Game", game_id)
            player_key = self.ds_client.key("Player", player_id, parent=game_key)
            player = self.ds_client.get(player_key)

            if source_deck not in player["decks"]:
                raise Exception(f"Player deck not found: {source_deck}")

            if destination_deck not in player["decks"]:
                raise Exception(f"Player deck not found: {destination_deck}")

            # if not virtual_dealer.cards.is_card_in_deck(player["decks"][source_deck], card):
            if card not in player["decks"][source_deck]:
                cards = player["decks"][source_deck]
                raise Exception(f"Card: {card} not in deck: {source_deck} {cards}")

            player["decks"][source_deck].remove(card)
            player["decks"][destination_deck].append(card)

            player["timestamp_updated"]: datetime.datetime.now()
            self.ds_client.put(player)
