"""
Tests for main.py
"""
import pytest
import main


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
    assert 200, response.status_code


def test_new_game_get(client):
    """
    Test GET /api/game/new
    """
    response = client.get("/api/game/new")
    assert 400, response.status_code
