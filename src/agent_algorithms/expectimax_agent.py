from agent_algorithms.agent import Agent

class ExpectimaxAgent(Agent):
    def get_face_combos(self, sum, die1, die2) -> list:
        all_pairs = [(x, sum - x) for x in range(max(1, sum - 6), min(6, sum - 1) + 1)]

        valid_pairs = [
            p for p in all_pairs 
            if p[0] in die1 and p[1] in die2
        ]
        return valid_pairs
    
    # Pass the list of all possible sums at the end of the search tree. Include duplicates to weight the probability
    # Time complexity is O(n) where n is the number of possible_sums given
    def get_best_value(self, possible_sums):
        max_win = float('-inf')
        best_guess = 0
        for i in range(2, 13):
            current_avg = 0.00
            for possible_sum in possible_sums:
                payout = self.session.calc_payout(i, possible_sum)
                current_avg += payout
            current_avg /= len(possible_sums)
            if current_avg > max_win:
                max_win = current_avg
                best_guess = i
        return best_guess
    
    def get_action(self, peeks):
        pass