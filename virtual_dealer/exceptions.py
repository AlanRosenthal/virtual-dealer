"""
Custom exceptions
"""


class InvalidMove(Exception):
    """
    Invalid move
    """

    def __init__(self, message):
        super(InvalidMove, self).__init__(message)
        self.message = message

    def __str__(self):
        return f"Invalid move: {self.message}"
