# Class for game logic of Sheng Ji
import numpy as np

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
            newPlayer = Player(i, (i + 2) % 4, 2)
            self.players.append(newPlayer)
            if i % 2 == 0:
                newPlayer.set_is_dealer(True)

        self.next_round_level = Level.TWO
        self.dealer = 0
        self.trump_suit = 'S'
        # TODO implement initial trump suit from dealer (potential)
        self.game_round = ShengJiGameRound(self.players, self.next_round_level, self.trump_suit, self.dealer)
        self.judger = ShengJiJudger(42)
        self.game_round_winners = None
        self.payoffs = np.zeros(4)
        return self.get_state(0), 0

    def step(self, action):
        self.game_round.proceed_round(action)
        if self.game_round.is_over:
            self.game_round_winners = self.judger.find_game_round_winners(self.players, self.game_round.total_offensive_points)
            self.update_payoffs()
            self.next_round_level = self.players[self.game_round_winners[0]].level # update next game round level using level of winners
            if self.is_over():
                self.winner_ids = self.judger.judge_game(self.players)
            else:
                self.dealer = self.find_dealers()
                self.game_round = ShengJiGameRound(self.players, self.next_round_level, self.trump_suit, self.dealer)
        next_player = self.game_round.get_next_player()
        next_state = self.get_state(next_player)
        return next_state, next_player

    def update_payoffs(self):
        payoffs = self.game_round.get_payoffs()
        for i in range(4):
            if i in self.game_round_winners:
                payoffs[i] += 1
            else:
                payoffs[i] -= 1
        self.payoffs = self.payoffs + payoffs


    def get_state(self, player_id):
        state = self.players[player_id].get_state()
        state["seen_cards"] = self.game_round.get_state()
        return state

    def find_dealers(self):
        if self.players[self.dealer].is_dealer:
            return (self.dealer + 2) % 4
        else:
            return (self.dealer + 1) % 4

    def is_over(self):
        for p in self.players:
            if p.level > 3:
                return True
        return False

    def get_payoffs(self):
        # getting point round payoffs from game round
        return self.payoffs
            # if not self.players[i].is_dealer and i in self.game_round_winners:
            #     payoffs[i] += 2 if self.game_round.total_offensive_points >= 120 else 1
            # elif i in self.game_round_winners:
            #     payoffs[i] += 2 if self.game_round.total_offensive_points == 0 else 1
            # else:
            #     payoffs[i] -= 1

        return payoffs

    def get_num_players(self):
        return 4

    def get_num_actions(self):
        return 54

    def get_player_id(self):
        return self.game_round.point_round.current_player







