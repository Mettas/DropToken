from game_token import GameToken
from exception import InvalidMoveException

class BoardColumn:
    """Represents a single column in a DropTokenGame."""

    def __init__(self, position, height):
        """Arguments:
        position -- int column number where this BoardColumn is located on the board
        height -- int max number of tokens allowed
        """
        self.tokens = []
        self.position = position
        self.height = height

    def add_token(self, player):
        """Creates and adds a token to this column.

        Arguments:
        player -- str name of player who is adding the token
        
        Returns the new GameToken
        """
        y = len(self.tokens)
        if y == self.height:
            raise InvalidMoveException("Column {} is full.".format(self.position))
        token = GameToken(self.position, y, player)
        self.tokens.append(token)
        return token

    def get_position(self, position):
        return self.position

    def get_token(self, index):
        """Retrieve GameToken at index

        Arguments:
        index -- int location of the token

        Returns a token if found, None otherwise
        """
        if index < 0 or index >= len(self.tokens):
            return None
        return self.tokens[index]

    def is_full(self):
        """Returns True if no more tokens can be added to this column"""
        return len(self.tokens) == self.height
