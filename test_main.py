"""
Tests for main.py
"""
import pytest
import main
import json


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
    response = client.post("/api/game/new")
    assert response.status_code == 201
    assert "game_id" in json.loads(response.data)
