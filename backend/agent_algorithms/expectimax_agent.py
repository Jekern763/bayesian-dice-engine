from agent_algorithms.agent import Agent


class ExpectimaxAgent(Agent):
    def get_face_combos(self, sum: int, die1: list, die2: list) -> list:
        all_pairs = [(x, sum - x) for x in range(max(1, sum - 6), min(6, sum - 1) + 1)]

        valid_pairs = [p for p in all_pairs if p[0] in die1 and p[1] in die2]
        return valid_pairs

    # Pass the list of all possible sums at the end of the search tree. Include duplicates to weight the probability
    # Time complexity is O(n) where n is the number of possible_sums given
    def get_best_value(self, possible_sums: list) -> float:
        max_win = float("-inf")
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

    def get_all_possible_sums(
        self,
        peeks: list,
        remaining_faces1: list,
        remaining_faces2: list,
        current_depth: int = 0,
        max_depth: int = 10,
    ) -> list:
        if current_depth > max_depth:
            raise RuntimeError(f"Recursive search passed max depth of {max_depth}")
        # if we have reached the bottom of the tree
        # current depth = 0 for first peek
        if current_depth == self.session.num_peeks:
            final_sums = []
            for f1 in remaining_faces1:
                for f2 in remaining_faces2:
                    final_sums.append(f1 + f2)
            return final_sums

        master_list_for_this_node = []

        observed_sum = peeks[current_depth]

        valid_pairs = self.get_face_combos(
            observed_sum, remaining_faces1, remaining_faces2
        )

        for face1, face2 in valid_pairs:
            next_faces1 = [f for f in remaining_faces1 if f != face1]
            next_faces2 = [f for f in remaining_faces2 if f != face2]

            returned_sums = self.get_all_possible_sums(
                peeks, next_faces1, next_faces2, current_depth + 1, max_depth
            )

            master_list_for_this_node.extend(returned_sums)

        return master_list_for_this_node

    def get_action(self, peeks):
        die1 = list(range(1, 7))
        die2 = list(range(1, 7))
        possible_sums = self.get_all_possible_sums(peeks, die1, die2)
        best_choice = self.get_best_value(possible_sums)
        return best_choice
