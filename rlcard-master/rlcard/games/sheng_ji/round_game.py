
from .round_point import ShengJiPointRound
from .judger import ShengJiJudger
from .dealer import ShengJiCardDealer

class ShengJiGameRound():

    def __init__(self, players, dealer_level, trump_suit, starting_player):
        self.point_round = ShengJiPointRound(dealer_level, trump_suit, starting_player)
        self.players = players
        self.level = dealer_level
        self.trump_suit = trump_suit
        self.starting_player = starting_player
        self.total_offensive_points = 0
        self.cards_left_to_play = 108
        self.is_over = False
        self.card_dealer = ShengJiCardDealer(self.players)
        self.card_dealer.deal_cards(self.players)
        # TODO random seed?
        self.judger = ShengJiJudger(42)

    def proceed_round(self, action):
        self.point_round.proceed_round(action, self.players)
        self.cards_left_to_play -= 1
        # checking if the point round ends after this play
        if self.point_round.is_over():
            winning_player = self.judger.find_point_round_winner(self.point_round.cards_played, self.starting_player,
                                                                 self.trump_suit, self.level)
            # is the winning player an offensive player?
            if not self.players[winning_player].is_dealer:
                self.total_offensive_points += self.point_round.get_points()
            # reset point round, next starting player is winning player
            self.point_round = ShengJiPointRound(self.level, self.trump_suit, winning_player)
        # check if this game round is over
        if self.cards_left_to_play == 0:
            self.is_over = True

    def get_winners(self):
        return self.judger.find_game_round_winners(self.players, self.total_offensive_points)

    def get_state(self):
        return self.point_round.get_state()

    def get_next_player(self):
        return self.point_round.current_player













