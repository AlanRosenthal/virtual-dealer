"""
Functional test for main.py
"""
import pytest
import requests

SERVER_URL = "http://127.0.0.1:8080"


def get_game_decks(game_id):
    """
    Print game's deck info
    """
    response = requests.get(
        f"{SERVER_URL}/api/game/{game_id}/deck/list", json={"name": "stock"}
    )
    assert response.status_code == 200
    print(f"game: {game_id}")

    data = response.json()
    for deck in data:
        print(f"    {deck['name']}: {deck['cards']}")

    return data


def get_player_decks(game_id, player_id):
    """
    Print player's deck info
    """
    response = requests.get(
        f"{SERVER_URL}/api/game/{game_id}/player/{player_id}/deck/list"
    )
    assert response.status_code == 200
    print(f"game: {game_id} player: {player_id}")
    data = response.json()
    for deck in data:
        print(f"    {deck['name']}: {deck['cards']}")

    return data


@pytest.mark.skip
def test_create_game():
    """
    Test creating a game, adding players and decks
    """
    print("Creating game!")

    response = requests.post(f"{SERVER_URL}/api/game/new")
    assert response.status_code == 201
    data = response.json()
    game_id = data["game_id"]
    print(f"game_id: {game_id}")

    response = requests.post(
        f"{SERVER_URL}/api/game/{game_id}/player/new",
        json={"name": "Alan", "email": "alan@fake.com"},
    )
    assert response.status_code == 201
    data = response.json()
    player1_id = data["player_id"]
    print(f"Adding player 1: player_id: {player1_id}")

    response = requests.post(
        f"{SERVER_URL}/api/game/{game_id}/player/new",
        json={"name": "Debbie", "email": "debbie@fake.com"},
    )
    assert response.status_code == 201
    data = response.json()
    player2_id = data["player_id"]
    print(f"Adding player 2: player_id: {player2_id}")

    response = requests.post(
        f"{SERVER_URL}/api/game/{game_id}/deck/new",
        json={"name": "stock", "is_full": True},
    )
    assert response.status_code == 201

    response = requests.post(
        f"{SERVER_URL}/api/game/{game_id}/deck/new", json={"name": "crib"}
    )
    assert response.status_code == 201

    response = requests.post(
        f"{SERVER_URL}/api/game/{game_id}/deck/new", json={"name": "starter_card"}
    )
    assert response.status_code == 201

    response = requests.post(
        f"{SERVER_URL}/api/game/{game_id}/player/{player1_id}/deck/new",
        json={"name": "hand"},
    )
    assert response.status_code == 201

    response = requests.post(
        f"{SERVER_URL}/api/game/{game_id}/player/{player1_id}/deck/new",
        json={"name": "discard_pile"},
    )
    assert response.status_code == 201

    response = requests.post(
        f"{SERVER_URL}/api/game/{game_id}/player/{player2_id}/deck/new",
        json={"name": "hand"},
    )
    assert response.status_code == 201

    response = requests.post(
        f"{SERVER_URL}/api/game/{game_id}/player/{player2_id}/deck/new",
        json={"name": "discard_pile"},
    )
    assert response.status_code == 201

    game_deck_stock_id = None
    game_decks = get_game_decks(game_id)
    for deck in game_decks:
        if deck["name"] == "stock":
            game_deck_stock_id = deck["deck_id"]
    assert game_deck_stock_id is not None

    player1_hand = None
    player1_deck = get_player_decks(game_id, player1_id)
    for deck in player1_deck:
        if deck["name"] == "hand":
            player1_hand = deck["deck_id"]
    assert player1_hand is not None

    response = requests.post(
        f"{SERVER_URL}/api/game/{game_id}/card/move",
        json={
            "cards": [{"rank": "A", "suit": "Club"}, {"rank": "A", "suit": "Heart"}],
            "source": {"deck_id": game_deck_stock_id},
            "destination": {"player_id": player1_id, "deck_id": player1_hand},
        },
    )
    assert response.status_code == 204

    player1_deck = get_player_decks(game_id, player1_id)
