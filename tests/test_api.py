"""
Tests for api.py
"""
import json


def test_root(client):
    """
    Start with a blank database.
    """

    response = client.get("/")
    assert {"message": "Hello"}, response.data
    assert response.status_code == 200


def test_post_api_game_new(client, store):
    """
    Test POST /api/game/new
    """
    store.create_new_game.return_value = {"game_id": 5}

    response = client.post("/api/game/new")
    data = json.loads(response.data)

    store.create_new_game.assert_called_once_with()
    assert response.status_code == 201
    assert data["game_id"] == 5


def test_get_api_game_gameid(client, store):
    """
    Test GET /api/game/<int:game_id>
    """
    store.get_game.return_value = None

    response = client.get("/api/game/5")

    store.get_game.assert_called_once_with(5)
    assert response.status_code == 200


def test_get_api_game_list(client, store):
    """
    Test GET /api/game/list
    """

    store.list_games.return_value = None

    response = client.get("/api/game/list")

    store.list_games.assert_called_once_with(10)
    assert response.status_code == 200


def test_get_api_game_list_count(client, store):
    """
    Test GET /api/game/list/<int:count>
    """

    store.list_games.return_value = None

    response = client.get("/api/game/list/234")

    store.list_games.assert_called_once_with(234)
    assert response.status_code == 200


def test_post_api_game_gameid_player_new(client, store):
    """
    Test POST /api/game/<int:game_id>/player/new
    """

    store.add_new_player_to_game.return_value = None

    response = client.post(
        "/api/game/3/player/new", json={"name": "Alan", "email": "fake@email.com"}
    )

    store.add_new_player_to_game.assert_called_once_with(3, "Alan", "fake@email.com")
    assert response.status_code == 201


def test_get_api_game_gameid_player_list(client, store):
    """
    Test GET /api/game/<int:game_id>/player/list
    """
    store.list_players.return_value = None

    response = client.get("/api/game/43/player/list")

    store.list_players.assert_called_once_with(43)
    assert response.status_code == 200


def test_get_api_game_gameid_player_playerid(client, store):
    """
    Test GET /api/game/<int:game_id>/player/<int:player_id>
    """
    store.get_player.return_value = None

    response = client.get("api/game/43/player/312")

    store.get_player.assert_called_once_with(43, 312)
    assert response.status_code == 200


def test_get_api_game_gameid_deck_new(client, store):
    """
    Test POST "/api/game/<int:game_id>/deck/new"
    """
    store.add_new_deck_to_game.return_value = True

    response = client.post("/api/game/3/deck/new", json={"name": "deck123"})

    store.add_new_deck_to_game.assert_called_once_with(3, "deck123", False)
    assert response.status_code == 201


def test_get_api_game_gameid_deck_new_full(client, store):
    """
    Test POST "/api/game/<int:game_id>/deck/new"
    """
    store.add_new_deck_to_game.return_value = True

    response = client.post(
        "/api/game/3/deck/new", json={"name": "deck123", "is_full": True}
    )

    store.add_new_deck_to_game.assert_called_once_with(3, "deck123", True)
    assert response.status_code == 201
