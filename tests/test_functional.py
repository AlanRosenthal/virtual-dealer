"""
Functional test for main.py
"""
import requests

SERVER_URL = "http://127.0.0.1:8080"


def print_game_deck_info(game_id):
    """
    Print game's deck info
    """
    response = requests.get(f"{SERVER_URL}/api/game/{game_id}")
    assert response.status_code == 200
    data = response.json()
    for deck, cards in data["decks"].items():
        print(f"game_id: {game_id}: Deck: {deck}: {len(cards)}: {cards}")


def print_player_deck_info(game_id, player_id):
    """
    Print player's deck info
    """
    response = requests.get(f"{SERVER_URL}/api/game/{game_id}/player/{player_id}")
    assert response.status_code == 200
    data = response.json()
    for deck, cards in data["decks"].items():
        print(
            f"game_id: {game_id}, player_id: {player_id}: Deck: {deck}: {len(cards)}: {cards}"
        )


# @pytest.mark.skip
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
        f"{SERVER_URL}/api/game/{game_id}/deck/new", json={"name": "crib"}
    )
    assert response.status_code == 201

    response = requests.post(
        f"{SERVER_URL}/api/game/{game_id}/deck/new", json={"name": "starter_card"}
    )
    assert response.status_code == 201

    print_game_deck_info(game_id)
    print_player_deck_info(game_id, player1_id)
    print_player_deck_info(game_id, player2_id)

    response = requests.post(
        f"{SERVER_URL}/api/game/{game_id}/move_cards/to_all_players",
        json={"game_deck": "stock", "player_deck": "hand", "card_count": 6},
    )
    assert response.status_code == 204

    print_game_deck_info(game_id)
    print_player_deck_info(game_id, player1_id)
    print_player_deck_info(game_id, player2_id)

    response = requests.get(f"{SERVER_URL}/api/game/{game_id}/player/{player1_id}")
    assert response.status_code == 200
    data = response.json()
    player1_hand = data["decks"]["hand"]

    response = requests.post(
        f"{SERVER_URL}/api/game/{game_id}/player/{player1_id}/move_card",
        json={
            "source_deck": "hand",
            "destination_deck": "discard_pile",
            "card": player1_hand[0],
        },
    )
    assert response.status_code == 204

    print_game_deck_info(game_id)
    print_player_deck_info(game_id, player1_id)
    print_player_deck_info(game_id, player2_id)
