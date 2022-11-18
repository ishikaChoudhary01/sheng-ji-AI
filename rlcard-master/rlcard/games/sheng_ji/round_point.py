from functools import reduce

class ShengJiPointRound():

    def __init__(self, level, trump_suit, starting_player):
        self.level = level
        self.starting_suit = None
        self.first_play = True
        self.trump_suit = trump_suit
        # current player index
        self.current_player = starting_player
        self.hand_winner = None
        self.cards_played = [None, None, None, None]
        self.round_over = False

    def proceed_round(self, action, players):
        if not self.first_play:
            self.starting_suit = action.suit
            self.first_play = False

        # getting the current player
        curr = players[self.current_player]
        # player plays card
        curr.play(action)
        self.cards_played[self.current_player] = action
        # update the other players' states with the new seen card
        # TODO: potentially just store the seen cards in the game itself because it's the same for all players
        for p in players:
            if p.get_player_index != self.current_player:
                p.add_seen_card(action, self.current_player)
        self.round_over
        self.round_over = reduce(lambda a,b: a is not None and b is not None, self.cards_played)
        if self.round_over:
            self.hand_winner = self.find_winner()

    # returns the player index of the winning player for this round
    # TODO implement a better way to compare cards
    def find_winner(self):
        winner = 0
        winning_card = self.cards_played[0]
        for i in range(4):
            card = self.cards_played[i]
            if card.suit == self.starting_suit and winning_card.suit == self.starting_suit:
                if card.rank > winning_card.rank:
                    winner = i
            if card.suit == self.trump_suit and winning_card.suit == self.starting_suit:
                winner = i
            if card.suit == self.trump_suit and winning_card.suit == self.trump_suit:
                if card.rank > winning_card.rank:
                    winner = i
        return winner


   