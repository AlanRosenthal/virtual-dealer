"""
pytest fixtures
"""
import unittest.mock as mock
import pytest
import virtual_dealer.api


@pytest.fixture(name="client")
def fixture_client():
    """
    Client test fixture for testing flask APIs
    """
    return virtual_dealer.api.app.test_client()


@pytest.fixture(name="store")
def fixture_store():
    """
    Mock for store::Store
    """
    with mock.patch("virtual_dealer.api.store", autospec=True) as mock_store:
        yield mock_store
