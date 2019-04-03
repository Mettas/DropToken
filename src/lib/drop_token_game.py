from board import Board
from move import Move
from move_type import MoveType
from game_state import GameState
from exception import GameEndedException, PlayerNotFoundException, NotYourTurnException, MovesNotFoundException, DuplicatePlayersException


# Represents how many tokens a player needs in a row to win
# We could potentially make it a parameter to the game for more flexibility
MATCHES = 4


class DropTokenGame:
    """Class that represents a drop-token game."""

    def __init__(self, width, height, players, game_id):
        """Arguments
        width -- int number of columns on the board
        height -- int number of rows on the board
        players -- list of participating players
        game_id -- str id/name of this game
        """
        self.board = Board(width, height)
        # Simple way of checking for duplicates in a python list
        if len(players) != len(set(players)):
            raise DuplicatePlayersException("All player names should be unique.")
        self.players = players
        self.winner = None
        self.moves_log = []
        self.game_id = game_id
        # We could potentially have additional game states
        # For example, a STARTING state where players can still join but not move
        self.game_state = GameState.IN_PROGRESS
        # Keeps track of who's turn it is
        # We start with the first name in players
        self.curr_player_idx = 0


    def get_game_id(self):
        return self.game_id


    def get_winner(self):
        return self.winner


    def get_players(self):
        return self.players


    def get_game_state(self):
        return self.game_state


    def get_board(self):
        return self.board


    def get_all_moves_taken(self, start=None, end=None):
        """Get a list of moves taken

        Arguments
        start -- optional int index of the first move to get. If None, will be 0
        end -- optional int index of the last move to get. If None, will be the index of the last move
        
        Returns a list of Moves from start to end inclusive
        """
        moves = len(self.moves_log)
        if moves == 0:
            raise MovesNotFoundException("No moves made thus far.")
        if start is None:
            start = 0
        if end is None:
            end = moves-1
        if start < 0 or start >= end or end >= moves:
            raise MovesNotFoundException("Moves {} to {} not found. Current total moves: {}.".format(start, end, moves))

        return self.moves_log[start:end+1]


    def get_move(self, move_number):
        """Gets the move at move_number

        Arguments:
        move_number -- index of the move to retrieve

        Returns a Move
        """
        if move_number < 0 or move_number >= len(self.moves_log):
            raise MovesNotFoundException("Move '{}' not found.".format(move_number))
        return self.moves_log[move_number]
    

    def remove_player(self, player):
        """Remove player (player quits) from the game.
        
        Arguments
        player -- player to remove

        return the Move representing the quit
        """
        if self.game_state == GameState.DONE:
            raise GameEndedException("Can't remove player; Game already ended")
        
        if player not in self.players:
            raise PlayerNotFoundException("{} not found in game {}".format(player, self.game_id))

        self.players.remove(player)
        # If it was that player's turn, we move on to the next player
        self.curr_player_idx %= len(self.players)
        move = Move(MoveType.QUIT, player, len(self.moves_log))
        self.moves_log.append(move)
        # As per the spec, no point in continuing a game with only 1 player
        if len(self.players) == 1:
            self.game_state = GameState.DONE
            self.winner = self.players[0]
        return move


    def play_token(self, player, col):
        """Add a new GameToken to the GameBoard.

        Arguments
        player -- player adding the token
        col -- int column that the token should be put in

        Retuns a new Move that represents this action
        """
        if self.game_state != GameState.IN_PROGRESS:
            raise NotYourTurnException("Game is currently '{}', no moves allowed.".format(self.game_state.name))

        if player not in self.players:
            raise PlayerNotFoundException("Player '{}' not part of game.".format(player))

        next_player = self.players[self.curr_player_idx]
        if player != next_player:
            raise NotYourTurnException("{}, its not your turn! Next player is {}".format(player, next_player))

        token = self.board.add_token(player, col)

        if self._is_winning_token(token):
            self.winner = token.get_player()
            self.game_state = GameState.DONE
        # If there is a winner as the board becomes full, we shouldn't draw
        elif self.board.is_full():
            self.game_state = GameState.DONE

        move = Move(MoveType.MOVE, player, len(self.moves_log), token)
        self.moves_log.append(move)

        # Move to the next player in line
        self.curr_player_idx = (self.curr_player_idx + 1) % len(self.players)
        
        return move


    def _is_winning_token(self, token):
        """Checks if there are more thant MATHCES consecutive matching tokens in a row.
        Looks in every direction (horizontal, verticle, right diagonal, left diagonal). 
        """
        # horizontal, verticle, right diagonal, left diagonal respectively
        return self._find_matching_consecutive_tokens(token, 1, 0) >= MATCHES  \
                or self._find_matching_consecutive_tokens(token, 0, 1) >= MATCHES  \
                or self._find_matching_consecutive_tokens(token, 1, 1) >= MATCHES  \
                or self._find_matching_consecutive_tokens(token, 1, -1) >= MATCHES
        
       
    def _find_matching_consecutive_tokens(self, token, x_diff, y_diff):
        """Looks at most MATCHES number of spots in each of 2 opposite directions:
        +x_diff, +y_diff and -x_diff, -y_diff.
        """
        found = 0
        x = token.get_column()
        y = token.get_row()
        # We only need to look at at most MATCHES spots
        # Any more matches than that are pointless
        for i in xrange(MATCHES):
            # If we find a token of another player, no point in continuing
            if not token.has_same_player(self.board.get_token(x, y)):
                break
            found += 1
            x += x_diff
            y += y_diff

        # We already counted the current played token above, so we start at 1 position further
        # Otherwise, identical to above besides subtracting x_diff and y_diff instead of adding 
        # (thus moving in the opposite diection)
        x = token.get_column() - x_diff
        y = token.get_row() - y_diff
        for i in xrange(MATCHES):
            if not token.has_same_player(self.board.get_token(x, y)):
                break
            found += 1
            x -= x_diff
            y -= y_diff
        return found 


