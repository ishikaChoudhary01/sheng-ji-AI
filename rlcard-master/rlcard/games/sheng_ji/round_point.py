from .judger import ShengJiJudger

# Represents one round where each player plays one card
class ShengJiPointRound():

    def __init__(self, level, trump_suit, starting_player):
        self.level = level
        self.starting_suit = None
        self.first_play = True
        self.trump_suit = trump_suit
        self.starting_player = starting_player
        # current player index
        self.current_player = starting_player
        self.hand_winner = None
        self.cards_played = [None, None, None, None]
        self.round_over = False
        # points currently out on the board
        self.points = 0
        # TODO should we change this?
        self.judger = ShengJiJudger(42)

    def proceed_round(self, action, players):
        if self.first_play:
            self.starting_suit = action.suit
            self.first_play = False
        # updating points
        if action.rank == '5':
            self.points += 5
        if action.rank == '10' or action.rank == 'K':
            self.points += 10
        # getting the current player
        curr = players[self.current_player]
        # player plays card
        curr.play(action)
        self.cards_played[self.current_player] = action
        self.round_over = True if self.current_player == (self.starting_player - 1) % 4 else False
        if self.round_over:
            self.hand_winner = self.judger.find_winner(self.cards_played, self.starting_player, self.trump_suit)
        else:
            # setting current player to next player
            self.current_player = (self.current_player + 1) % 4

    def get_points(self):
        return self.points

    def is_over(self):
        return self.round_over

    def get_state(self):
        return self.cards_played


