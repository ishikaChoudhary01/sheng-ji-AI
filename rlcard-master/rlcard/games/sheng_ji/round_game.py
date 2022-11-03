
class ShengJiGameRound():

    def __init__(self, players, dealer_level, trump_suit, starting_player):
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
