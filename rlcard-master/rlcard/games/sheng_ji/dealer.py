# Deals cards to four players according to Level Up rules

import functools

from rlcard.utils import init_54_deck

class ShengJiCardDealer:
    ''' Dealer will shuffle, deal cards, and determine players' roles
    '''
    def __init__(self, np_random):
        '''Give dealer the deck

        Notes:
            1. deck with 54 cards including black joker and red joker
        '''
        self.np_random = np_random
        self.deck = init_54_deck().extend(init_54_deck())

    def shuffle(self):
        ''' Randomly shuffle the deck
        '''
        self.np_random.shuffle(self.deck)

    def deal_cards(self, players):
        ''' Deal cards to players

        Args:
            players (list): list of Sheng Ji Player objects
        '''
        # not doing bottom pile!
        playable_len = len(self.deck)
        for player in players:
            player.set_hand(self.deck[player.get_player_index(): playable_len:4])
