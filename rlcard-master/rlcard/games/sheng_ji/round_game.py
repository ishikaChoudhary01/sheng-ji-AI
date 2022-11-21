
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
        self.cards_left_to_play = 26
        self.is_over = False
        
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
            self.cards_left_to_play -= 1
        # check if this game round is over
        if self.cards_left_to_play == 0:
            self.is_over = True
            # TODO check what number this should be
            if self.total_offensive_points < 50:
                self.did_dealers_win = True

    def find_winners(self):
        winners = []
        for p in self.players:
            if self.did_dealers_win:
                if p.is_dealer:
                    winners.append(p)
            else:
                if not p.is_dealer:
                    winners.append(p)

        winner_score = 200 - self.total_offensive_points if self.did_dealers_win else self.total_offensive_points

        return self.did_dealers_win, winners, winner_score











