
class ShengJiPlayer:

    def __init__(self, player_index, teammate_index):
        self.player_index = player_index
        self.hand = []
        self.role = None
        self.teammate = teammate_index
        self.level = 2
        self.trump_suit = 'S'

    def level_up(self, num_levels):
        self.level += num_levels

    def set_role(self, role):
        self.role = role

    def set_hand(self, new_hand):
        self.hand = new_hand

    def play(self, card):
        self.hand.remove(card)
        #TODO: what to return here?? if anything? add card to state?

    def available_actions(self, suit_in_play, current_level):
        possible_plays = [card for card in self.hand if card.suit == suit_in_play and card.rank != current_level]

        if len(possible_plays) == 0:
            return self.hand
        else:
            return possible_plays


