class GameToken:
    def __init__(self, col, row, player):
        self.col = col
        self.row = row
        self.player = player
    
    def get_column(self):
        return self.col

    def get_row(self):
        return self.row

    def get_player(self):
        return self.player

    def has_same_player(self, token):
        return token is not None and self.player == token.player
