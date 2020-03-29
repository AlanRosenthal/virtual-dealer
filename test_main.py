"""
Tests for main.py
"""
import json
import unittest.mock as mock
import pytest
import main


@pytest.fixture(name="client")
def fixture_client():
    """
    Client test fixture for testing flask APIs
    """
    return main.app.test_client()


@pytest.fixture(name="store")
def fixture_store():
    """
    Mock for store::Store
    """
    # return_value = {"game_id": 5}
    with mock.patch("main.store", autospec=True) as mock_store:
        yield mock_store


def test_root(client):
    """
    Start with a blank database.
    """

    response = client.get("/")
    assert {"message": "Hello"}, response.data
    assert response.status_code == 200


def test_new_game_get(client):
    """
    Test GET /api/game/new
    """
    response = client.get("/api/game/new")
    assert response.status_code == 405


def test_new_game_post(client, store):
    """
    Test POST /api/game/new
    """
    store.create_new_game.return_value = {"game_id": 5}

    response = client.post("/api/game/new")
    data = json.loads(response.data)

    assert store.create_new_game.assert_called_once
    assert response.status_code == 201
    assert "game_id" in data
    assert data["game_id"] == 5
