
class ShengJiPlayer:

    def __init__(self, player_index, teammate_index, level, trump_suit):
        self.player_index = player_index
        self.hand = []
        self.is_dealer = False
        self.teammate = teammate_index
        self.level = level
        self.trump_suit = trump_suit
        self.seen_cards = []

    def get_state(self):
        state = {}
        state['hand'] = self.hand
        state['seen_cards'] = self.seen_cards
        return state

    def get_player_index(self):
        return self.player_index

    def level_up(self, num_levels):
        self.level += num_levels

    def set_role(self, is_dealer):
        self.role = is_dealer

    def switch_role(self):
        self.is_dealer = not self.is_dealer

    def set_hand(self, new_hand):
        self.hand = new_hand

    def play(self, card):
        self.hand.remove(card)
        self.seen_cards[self.player_index] = card

    # Adds new observed card to this player's seen card (not for when the player plays their own card)
    def add_seen_card(self, card, player_index):
        self.seen_cards[player_index] = card

    def available_actions(self, suit_in_play, current_level):
        possible_plays = [card for card in self.hand if card.suit == suit_in_play and card.rank != current_level]

        if len(possible_plays) == 0:
            return self.hand
        else:
            return possible_plays

