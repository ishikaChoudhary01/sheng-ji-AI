import numpy as np
from rlcard.envs import Env
from rlcard.games.sheng_ji import ShengJiGame
from rlcard.utils import init_54_deck


class ShengJiEnv(Env):

    def __init__(self, config):
        self.name = 'sheng-ji'
        self.game = ShengJiGame()
        #self.game.init_game()
        super().__init__(config)
        # hand, cards on table, level
        # TODO figure out how to define state shape
        # up to 27 cards in player's hand + up to 4 seen cards (31 5*1 feature planes) + 1 level (encoded in 5*1 plane)
        # 5 represents card 1-hot
        self.state_shape = [[32, 5] for _ in range(self.num_players)]
        self.action_shape = [[54] for _ in range(self.num_players)]
        self.card_to_action = init_54_deck()
        self.rank2number = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
                            "Q": 12, "K": 13, "A": 14, "BJ": 15, "RJ": 16}


    def get_payoffs(self):
        ''' Get the payoffs of players.

        Returns:
            (list): A list of payoffs for each player.

        '''
        return self.game.get_payoffs()


    def _extract_state(self, state):
        ''' Extract useful information from state for RL.

        Args:
            state (dict): The raw state

        Returns:
            (numpy.array): The extracted state
        '''
        obs = self.extract_obs(state)
        extracted_state = {}
        extracted_state['obs'] = obs
        extracted_state['raw_obs'] = state
        extracted_state['legal_actions'] = self.extract_legal_actions()
        curr_game_round = self.game.game_round
        extracted_state['raw_legal_actions'] = self.game.players[curr_game_round.point_round.current_player]\
            .get_legal_actions(curr_game_round.trump_suit, curr_game_round.point_round.starting_suit, curr_game_round.level)
        return extracted_state


    def extract_legal_actions(self):
        curr_game_round = self.game.game_round
        legal_actions = self.game.players[curr_game_round.point_round.current_player].\
            get_legal_actions(curr_game_round.trump_suit,curr_game_round.point_round.starting_suit, curr_game_round.level)
        return {self.card_to_action.index(action): self.card_to_array(action) for action in legal_actions}

    def card_to_array(self, card):
        if card == None:
            return [0,0,0,0,0]
        if card.suit == 'S':
             return [1, 0, 0, 0, self.rank2number[card.rank]]
        elif card.suit == 'C':
            return [0, 1, 0, 0, self.rank2number[card.rank]]
        elif card.suit == 'H':
            return [0, 0, 1, 0, self.rank2number[card.rank]]
        elif card.suit == 'D':
            return [0, 0, 0, 1, self.rank2number[card.rank]]
        elif card.suit == "RJ" or card.suit == "BJ":
            return [1, 0, 0, 0, self.rank2number[card.suit]]


    def extract_obs(self, state):
        def card_array_to_number(cards, expected_len):
            result = []
            for c in cards:
                result.extend(self.card_to_array(c))
            if len(result) < expected_len:
                result.extend(np.zeros(expected_len - len(result)))
            return result

        hand = state['hand']
        level = state['level']
        seen_cards = state['seen_cards']
        no_played_cards = True
        for card in seen_cards:
            if card != None:
                no_played_cards = False
        if no_played_cards:
            # 4 cards, 5 numbers per card
            seen_cards = np.zeros(20)
        else:
            seen_cards = card_array_to_number(seen_cards, 4*5)
        cards = card_array_to_number(hand, 27*5)
        cards.extend([0,0,0,0,level])
        cards.extend(seen_cards)

        return cards


    def _decode_action(self, action_id):
        ''' Decode Action id to the action in the game.

        Args:
            action_id (int): The id of the action

        Returns:
            (string): The action that will be passed to the game engine.

        '''
        return self.card_to_action[action_id]


    def _get_legal_actions(self):
        ''' Get all legal actions for current state.

        Returns:
            (list): A list of legal actions' id.

        '''
        curr_game_round = self.game.game_round
        legal_actions = curr_game_round.point_round.current_player.get_legal_actions(curr_game_round.trump_suit, curr_game_round.point_round.suit_in_play, game_round.level)
        #if legal_actions:
