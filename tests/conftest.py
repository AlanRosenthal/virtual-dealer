"""
pytest fixtures
"""
import pytest
import main


@pytest.fixture(name="client")
def fixture_client():
    """
    Client test fixture for testing flask APIs
    """
    return main.app.test_client()
