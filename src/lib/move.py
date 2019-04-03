class Move:
    def __init__(self, move_type, player, move_number, token=None):
        self.token = token
        self.type = move_type
        self.player = player
        self.move_number = move_number
    
    def get_type(self):
        return self.type

    def get_player(self):
        return self.player

    def get_token(self):
        return self.token

    def get_move_number(self):
        return self.move_number
