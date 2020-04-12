"""
Helper functions for cards
"""
import random


def create_full_deck():
    """
    Return a list of all cards in a deck
    """
    cards = []
    suits = ["Heart", "Diamond", "Spade", "Club"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    for suit in suits:
        for rank in ranks:
            cards.append({"rank": rank, "suit": suit})

    return cards


def shuffle_deck(deck):
    """
    Shuffle desk
    """
    return random.shuffle(deck)
