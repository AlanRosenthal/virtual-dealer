"""
Tests for main.py
"""
import json
import unittest.mock as mock
import main
import pytest


@pytest.fixture(name="client")
def fixture_client():
    """
    Client test fixture for testing flask APIs
    """
    return main.app.test_client()


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


def test_new_game_post(client):
    """
    Test POST /api/game/new
    """
    with mock.patch(
        "store.Store.create_new_game",
        mock.MagicMock(return_value={"game_id": 5}),
        spec=True,
    ) as mock_create_new_game:
        response = client.post("/api/game/new")
        data = json.loads(response.data)
        assert mock_create_new_game.assert_called_once
        assert response.status_code == 201
        assert "game_id" in data
        assert data["game_id"] == 5
