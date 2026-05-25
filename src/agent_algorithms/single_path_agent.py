from agent_algorithms.agent import Agent
from random import choice

""" This agent will randomly select one path to follow.
In practice, this means it will choose one belief of what sides were rolled, and continue down that path
Could be compared to a simplified Monte Carlo Tree Search that only explores one path, and doesn't backtrack."""

class SinglePathAgent(Agent):
    def get_action(self, peeks:list, max_search_rounds:int=20) -> int:
        # Wrap the entire hallucination in a retry loop.
        # If we hit a dead end, we restart the simulation from round 1.
        round_counter = 0
        while round_counter < max_search_rounds:
            round_counter += 1
            # Fresh dice for a new timeline
            die1_belief = [1, 2, 3, 4, 5, 6]
            die2_belief = [1, 2, 3, 4, 5, 6]
            timeline_valid = True

            for peek in peeks:
                # Generate all mathematically possible pairs for this peek
                all_pairs = [(x, peek - x) for x in range(max(1, peek - 6), min(6, peek - 1) + 1)]

                #Filter to ONLY pairs that actually survive in our current belief state
                valid_pairs = [
                    p for p in all_pairs 
                    if p[0] in die1_belief and p[1] in die2_belief
                ]

                if not valid_pairs:
                    # hallucination trapped the algorithm. 
                    # Break the 'for' loop and let the 'while' loop restart.
                    timeline_valid = False
                    break

                # Pick a valid pair and cross those faces off the scratchpad
                chosen_pair = choice(valid_pairs)
                die1_belief.remove(chosen_pair[0])
                die2_belief.remove(chosen_pair[1])

            # If we made it through all the peeks without hitting a dead end, 
            # our hallucinated timeline is complete and mathematically sound!
            if timeline_valid:
                break

        possible_sums = [d1 + d2 for d1 in die1_belief for d2 in die2_belief]
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
        
        