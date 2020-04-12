import pytest
import main
import json


@pytest.fixture(name="client")
def fixture_client():
    """
    Client test fixture for testing flask APIs
    """
    return main.app.test_client()


def print_game_deck_info(client, game_id):
    response = client.get(f"/api/game/{game_id}")
    data = json.loads(response.data)
    for deck, cards in data["decks"].items():
        print(f"game_id: {game_id}: Deck: {deck}: {len(cards)}")


def print_player_deck_info(client, game_id, player_id):
    response = client.get(f"/api/game/{game_id}/player/{player_id}")
    data = json.loads(response.data)
    for deck, cards in data["decks"].items():
        print(f"game_id: {game_id}, player_id: {player_id}: Deck: {deck}: {len(cards)}")


def test_create_game(client):
    print("Creating game!")

    response = client.post("/api/game/new")
    data = json.loads(response.data)
    game_id = data["game_id"]
    print(f"game_id: {game_id}")

    player = {"name": "Alan", "email": "alan@fake.com"}
    response = client.post(f"/api/game/{game_id}/player/new", json=player)
    data = json.loads(response.data)
    player1_id = data["player_id"]
    print(f"Adding player 1: player_id: {player1_id}")

    player = {"name": "Debbie", "email": "debbie@fake.com"}
    response = client.post(f"/api/game/{game_id}/player/new", json=player)
    data = json.loads(response.data)
    player2_id = data["player_id"]
    print(f"Adding player 2: player_id: {player2_id}")

    print_game_deck_info(client, game_id)
    print_player_deck_info(client, game_id, player1_id)
    print_player_deck_info(client, game_id, player2_id)

    deck = {"name": "crib"}
    response = client.post(f"/api/game/{game_id}/deck/new", json=deck)
    data = json.loads(response.data)
    print(data)

    deck = {"name": "crib"}
    response = client.post(f"/api/game/{game_id}/deck/new", json=deck)
    data = json.loads(response.data)
    print(data)
    # print_game_deck_info(client, game_id)
