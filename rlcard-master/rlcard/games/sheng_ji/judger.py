import numpy as np

class ShengJiJudger:  
    
    def __init__(self, np_random):
        self.np_random = np_random

    #self, players, points, teams
    def judge_game(self, players, hands):
        """
        Judge the winner of the game.

        Args:
            players (list): The list of players who play the game
            hands (list): The list of hands that from the players

        Returns:
            (list): Each entry of the list corresponds to one entry of the
        """
        # Convert the hands into card indexes
        hands = [[card.get_index() for card in hand] if hand is not None else None for hand in hands]

        winners = compare_hands(hands)

        in_chips = [p.in_chips for p in players]
        each_win = self.split_pots_among_players(in_chips, winners)

        payoffs = []
        for i, _ in enumerate(players):
            payoffs.append(each_win[i] - in_chips[i])
        assert sum(payoffs) == 0
        return payoffs

    def find_point_round_winner(self, cards_played, starting_player, trump_suit):
        winner_index = starting_player
        winning_card = cards_played[starting_player]
        starting_suit = cards_played[starting_player].suit

        for i in range(4):
            curr_player = starting_player + i % 4
            card = cards_played[curr_player]
            # if highest card and current card both starting suit -> compare rank
            if card.suit == starting_suit and winning_card.suit == starting_suit:
                if card.rank > winning_card.rank:
                    winner_index = curr_player
                    winning_card = cards_played[curr_player]

            # if highest card starting suit but this card trump suit -> this card is new highest
            if card.suit == trump_suit and winning_card.suit == starting_suit:
                winner_index = curr_player
                winning_card = cards_played[curr_player]

            # if highest card and current card both trump suit -> compare rank
            if card.suit == trump_suit and winning_card.suit == trump_suit:
                if card.rank > winning_card.rank:
                    winner_index = curr_player
                    winning_card = cards_played[curr_player]

        return winner_index

    def find_game_round_winners(self, players, total_offensive_points):
        winners = []
        # if offense won
        if self.total_offensive_points >= 40:
            levels = 2 if total_offensive_points >= 120 else 1
            for p in players:
                if not p.is_dealer:
                    p.level_up(levels)
                    winners.append(p)
                p.switch_role()
        # if dealers won
        else:
            levels = 2 if total_offensive_points == 0 else 1
            for p in players:
                if p.is_dealer:
                    p.level_up(levels)
                    winners.append(p)

        return winners


