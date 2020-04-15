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


@pytest.fixture(name="datastore")
def fixture_datastore():
    """
    Client test fixture for testing Google's datastore APIs
    """
    with mock.patch("virtual_dealer.store.datastore", autospec=True) as mock_datastore:
        yield mock_datastore


@pytest.fixture(name="datastore_key")
def fixture_datastore_key():
    """
    Datastore Key Mock
    """
    return mock.MagicMock()


@pytest.fixture(name="datastore_entity")
def fixture_datastore_entity():
    """
    Datastore Entity Mock
    """
    return mock.MagicMock()
