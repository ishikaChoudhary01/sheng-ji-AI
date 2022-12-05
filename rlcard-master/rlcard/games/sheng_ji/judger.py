import numpy as np

class ShengJiJudger:  
    
    def __init__(self, np_random):
        self.np_random = np_random
        self.rank2number = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11,
                           "Q": 12, "K": 13, "A": 14, "BJ": 15, "RJ": 16}

    #self, players, points, teams
    def judge_game(self, players):
        return [p.player_index for p in players if p.level > 13]

    def find_point_round_winner(self, cards_played, starting_player, trump_suit, current_level):
        winner_index = starting_player
        winning_card = cards_played[starting_player]
        winning_card_value = self.rank2number[winning_card.suit] if winning_card.suit == 'BJ' or winning_card.suit == 'RJ' \
            else self.rank2number[winning_card.rank]
        starting_suit = cards_played[starting_player].suit
        if starting_suit == "BJ" or starting_suit == "RJ":
            starting_suit = trump_suit

        for i in range(4):
            curr_player = (starting_player + i) % 4
            card = cards_played[curr_player]
            card_value = self.rank2number[card.suit] if card.suit == 'BJ' or card.suit == 'RJ' else self.rank2number[card.rank]
            # if highest card and current card both starting suit -> compare rank
            if card.suit == starting_suit and winning_card.suit == starting_suit:
                if card_value > winning_card_value:
                    winner_index = curr_player
                    winning_card = cards_played[curr_player]
                    winning_card_value = self.rank2number[
                        winning_card.suit] if winning_card.suit == 'BJ' or winning_card.suit == 'RJ' \
                        else self.rank2number[winning_card.rank]

            # if played card is trump suit
            if (card.suit == trump_suit or card.suit == "RJ" or card.suit == "BJ" or card.rank == current_level):
                # winning card is not trump suit # OR both played and winning card are trump suit, so compare rank
                if (winning_card.suit == starting_suit) or \
                    (winning_card.suit == trump_suit or winning_card.suit == "RJ" 
                    or winning_card.suit == "BJ" or winning_card.rank == current_level) and card.rank > winning_card.rank:
                    winner_index = curr_player
                    winning_card = cards_played[curr_player]
                    winning_card_value = self.rank2number[
                        winning_card.suit] if winning_card.suit == 'BJ' or winning_card.suit == 'RJ' \
                        else self.rank2number[winning_card.rank]

        return winner_index

    def find_game_round_winners(self, players, total_offensive_points):
        winners = []
        # if offense won
        if total_offensive_points >= 40:
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


