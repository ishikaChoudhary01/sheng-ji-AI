# Class for game logic of Sheng Ji
from .player import ShengJiPlayer as Player
from .level import Level
from .role import Role

class ShengJiGame:

    def __init__(self):
        self.num_players = 4

    def init_game(self):
        self.winner_ids = []
        self.players = []
        for i in range(self.num_players):
            newPlayer = Player(i, (i + 2) % 4)
            self.players.append(newPlayer)
            if i % 2 == 0:
                newPlayer.set_role(Role.DEALER)
            else:
                newPlayer.set_role(Role.OFFENSE)

        self.level = Level.TWO
        self.dealer = 0

    def step(self, action):
        return None

    def get_state(self, player_id):
        return self.players[player_id].get_state()









