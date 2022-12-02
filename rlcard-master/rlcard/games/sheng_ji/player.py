
class ShengJiPlayer:

    def __init__(self, player_index, teammate_index, level, trump_suit):
        self.player_index = player_index
        self.hand = []
        self.is_dealer = False
        self.teammate = teammate_index
        self.level = level
        self.trump_suit = trump_suit


    def get_state(self):
        state = {}
        state['hand'] = self.hand
        state['level'] = self.level
        return state

    def get_player_index(self):
        return self.player_index

    def level_up(self, num_levels):
        self.level += num_levels

    def switch_role(self):
        self.is_dealer = not self.is_dealer

    # if this player is on the dealer team
    def set_is_dealer(self, is_dealer):
        self.is_dealer = is_dealer

    def set_hand(self, new_hand):
        self.hand = new_hand

    def play(self, card):
        self.hand.remove(card)

    def available_actions(self, suit_in_play, current_level):
        possible_plays = [card for card in self.hand if card.suit == suit_in_play and card.rank != current_level]

        if len(possible_plays) == 0:
            return self.hand
        else:
            return possible_plays

    def reset_seen_cards(self):
        self.seen_cards = []

