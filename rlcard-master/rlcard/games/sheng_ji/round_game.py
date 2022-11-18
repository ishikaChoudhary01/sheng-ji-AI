
from .round_point import ShengJiPointRound

class ShengJiGameRound():

    def __init__(self, players, dealer_level, trump_suit, starting_player):
        self.point_round = ShengJiPointRound(dealer_level, trump_suit, starting_player)
        self.players = players
        self.level = dealer_level
        self.trump_suit = trump_suit
        self.starting_player = starting_player
        self.final_hand_winner = None
        self.total_offensive_points = 0
        self.did_dealers_win = False
        
        if not starting_player.is_dealer:
            for player in players:
                player.switch_teams()

    def proceed_round(self, action):
        self.point_round.proceed_round(action, self.players)
        # checking if the round ends after this play
        if self.point_round.is_over():
            winning_player = self.point_round.find_winner()
            # TODO change to check if teammate of offense
            if not self.players[winning_player].is_dealer:
                self.total_offensive_points += self.point_round.get_points()
            # reset point round, next starting player is winning player
            self.point_round = ShengJiPointRound(self.level, self.trump_suit, winning_player)
        # check if this game round is over





