from board_column import BoardColumn
from exception import InvalidMoveException

class Board:
    """Class representing a DropTokenGame board"""

    def __init__(self, width, height):
        """Arguments
        width -- int number of columns on the board
        height -- int number of rows on the board
        """

        self.columns = {}
        self.width = width
        self.height = height
        # This will be used to help quickly determine if the board is full
        # It coud be a list, but making it a dictionary helps with fast deletes
        # if in the future we want to undo moves
        self.full_cols = {}


    def add_token(self, player, col):
        """Add a token to a BoardColumn on the board

        Arguments
        player -- str name of the player adding the token
        col -- int position of the column that will recieve the new token
        
        Returns the new GameToken
        """
        if not (0 <= col < self.width):
            raise InvalidMoveException("Move {} is not on the board.".format(col))

        if col not in self.columns:
            self.columns[col] = BoardColumn(col, self.height)

        token = self.columns[col].add_token(player)
        if self.columns[col].is_full():
            self.full_cols[col] = self.columns[col]
        return token


    def get_token(self, x, y):
        """Retrieve GameToken at index

        Arguments:
        index -- int location of the token

        Returns a token if found, None otherwise
        """
        if x not in self.columns:
            return None
        return self.columns[x].get_token(y)

    
    def is_full(self):
        """Returns True if no more tokens can be added to this board"""
        return len(self.full_cols) == self.width
