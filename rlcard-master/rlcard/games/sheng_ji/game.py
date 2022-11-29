# Class for game logic of Sheng Ji
from .player import ShengJiPlayer as Player
from .level import Level
from .role import Role
from .round_game import ShengJiGameRound

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
                newPlayer.set_is_dealer(True)

        self.level = Level.TWO
        self.dealer = 0
        # TODO what should starting trump suit be
        self.game_round = ShengJiGameRound(self.players, self.level, 'A', 0)

    def step(self, action):
        self.game_round.proceed_round(action)
        if self.game_round.is_over:
            round_results = self.game_round.find_winners()
            # TODO what level rules change
            # TODO who starts next
            self.game_round = ShengJiGameRound(self.players, self.level, 'A', 0)

    def get_state(self, player_id):
        state = self.players[player_id].get_state()
        state["seen_cards"] = self.game_round.get_state()
        return state









