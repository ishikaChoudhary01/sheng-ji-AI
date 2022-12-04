from rlcard.envs import Env
from rlcard.games.sheng_ji import ShengJiGame
from rlcard.utils import init_54_deck


class ShengJiEnv(Env):

    def __init__(self):
        self.name = 'sheng-ji'
        self.game = ShengJiGame()
        super().__init__(config)
        # hand, cards on table, level
        self.state_shape = [[130, 20, 1] for _ in range(self.num_players)]
        self.action_shape = [[54] for _ in range(self.num_players)]
        self.card_to_action = init_54_deck()


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
        obs = extract_obs(state)


    def extract_legal_actions(self):
        curr_game_round = self.game.game_round
        legal_actions = curr_game_round.point_round.current_player.get_legal_actions(curr_game_round.trump_suit, curr_game_round.point_round.suit_in_play, curr_game_round.level)
        return [self.card_to_action().index(action) for action in legal_actions]


    def extract_obs(self, state):
        def card_array_to_number(cards):
            result = []
            for c in cards:
                if c.suit == 'S':
                    result.extend([1, 0, 0, 0, c.rank])
                elif c.suit == 'C':
                    result.extend([0, 1, 0, 0, c.rank])
                elif c.suit == 'H':
                    result.extend([0, 0, 1, 0, c.rank])
                elif c.suit == 'D':
                    result.extend([0, 0, 0, 1, c.rank])
            return result

        hand = state['hand']
        level = state['level']
        seen_cards = state['seen_cards']
        return card_array_to_number(hand).append(level).extend(card_array_to_number(seen_cards))


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
