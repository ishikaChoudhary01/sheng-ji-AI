
class ShengJiPointRound():

    def __init__(self, level, trump_suit, starting_player):
        self.level = level
        self.trump_suit = trump_suit
        self.current_player = starting_player
        self.hand_winner = None
        self.cards_played = [None, None, None, None]
   