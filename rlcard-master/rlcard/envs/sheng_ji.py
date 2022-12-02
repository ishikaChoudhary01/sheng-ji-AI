from rlcard.envs import Env
from rlcard.games.sheng_ji import ShengJiGame


class ShengJiEnv(Env):

    def __init__(self):
        self.name = "sheng ji"
        self.game = ShengJiGame()


    def get_payoffs(self):
        ''' Get the payoffs of players.

        Returns:
            (list): A list of payoffs for each player.

        Note: Must be implemented in the child class.
        '''
        raise NotImplementedError


    def _extract_state(self, state):
        ''' Extract useful information from state for RL.

        Args:
            state (dict): The raw state

        Returns:
            (numpy.array): The extracted state
        '''
        raise NotImplementedError

    def _decode_action(self, action_id):
        ''' Decode Action id to the action in the game.

        Args:
            action_id (int): The id of the action

        Returns:
            (string): The action that will be passed to the game engine.

        '''
        raise NotImplementedError

    def _get_legal_actions(self):
        ''' Get all legal actions for current state.

        Returns:
            (list): A list of legal actions' id.

        '''
        raise NotImplementedError
