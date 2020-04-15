"""
Tests for store.py
"""
import virtual_dealer.store


def test_create_class(datastore):
    """
    Create a Store class
    """
    store = virtual_dealer.store.Store()
    datastore.Client.assert_called_once_with()

    assert store.ds_client


def test_create_new_game(datastore, datastore_key, datastore_entity):
    """
    Test store.create_new_game()
    """
    store = virtual_dealer.store.Store()
    store.ds_client.key.return_value = datastore_key
    datastore.Entity.return_value = datastore_entity
    datastore_entity.key.id = 123

    game = store.create_new_game()

    assert game["game_id"] == 123
    datastore.Client.assert_called_once_with()
    datastore.Client().key.assert_called_once_with("Game")
    datastore.Entity.assert_called_once_with(key=datastore_key)
    datastore.Entity().update.assert_called_once()
    datastore.Client().put.assert_called_once_with(datastore_entity)


def test_get_game(datastore, datastore_key, datastore_entity):
    """
    Test store.get_game()
    """
    store = virtual_dealer.store.Store()
    store.ds_client.key.return_value = datastore_key
    store.ds_client.get.return_value = datastore_entity

    game = store.get_game(123)

    assert game == datastore_entity
    datastore.Client.assert_called_once_with()
    datastore.Client().key.assert_called_once_with("Game", 123)
    datastore.Client().get.assert_called_once_with(datastore_key)
