# Class for game logic of Sheng Ji
from .player import ShengJiPlayer as Player
from .level import Level
from .round_game import ShengJiGameRound
from .judger import ShengJiJudger
from .dealer import ShengJiCardDealer

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
        self.card_dealer = ShengJiCardDealer(self.players)
        self.next_round_level = Level.TWO
        self.dealer = 0
        self.trump_suit = 'S'
        # TODO implement initial trump suit from dealer (potential)
        self.game_round = ShengJiGameRound(self.players, self.next_round_level, self.trump_suit, self.dealer)
        self.judger = ShengJiJudger(42)
        self.is_over = False

    def step(self, action):
        self.game_round.proceed_round(action)
        if self.game_round.is_over:
            self.game_round.find_winners()
            if self.is_game_over():
                self.winner_ids = self.judger.judge_game()
            else:
                self.dealer = self.find_dealers()
                self.game_round = ShengJiGameRound(self.players, self.next_round_level, self.trump_suit, self.dealer)
        next_player = self.game_round.get_next_player()
        next_state = self.get_state(next_player)
        return next_state, next_player


    def get_state(self, player_id):
        state = self.players[player_id].get_state()
        state["seen_cards"] = self.game_round.get_state()
        return state

    def find_dealers(self):
        if self.players[self.dealer].is_dealer:
            return self.dealer + 2 % 4
        else:
            return self.dealer + 1 % 4

    def is_game_over(self):
        for p in self.players:
            if p.level > 13:
                self.is_over = True
                return True
        return False

    def get_payoffs(self):
        payoffs = []
        for i in range(4):
            if i in self.winner_ids:
                payoffs[i] = 1
            else:
                payoffs[i] = -1
        return payoffs








