# quick setup for importing game
import sys
from collections import Counter
from collections.abc import Iterable
from itertools import product
from pathlib import Path
from statistics import mean, pvariance, variance

from analysis_by_dice_config import _weighted_mean
from pandas import DataFrame
from scipy.stats import entropy
from state_analysis import GameState, GraphAnalysis, analyze_state_graph
from state_graph import build_state_graph, create_initial_state

game_engine_dir = Path(
    "/Users/jamesekern/pythonProjects/gamblint/backend/game_engine"
).resolve()

module_dir = game_engine_dir.parent

if str(game_engine_dir) not in sys.path:
    sys.path.append(str(game_engine_dir))

if str(module_dir) not in sys.path:
    sys.path.insert(0, str(module_dir))

from game import Game  # type: ignore

instance = Game(1, 1)

calc_payout = instance.calc_payout


def _safe_variance(values: tuple[float, ...]) -> float:
    """Return sample variance, treating fewer than two values as zero."""
    if len(values) < 2:
        return 0.0

    return variance(values)


def _safe_pvariance(values: tuple[float, ...]) -> float:
    """Return population variance, treating fewer than two values as zero."""
    if len(values) < 2:
        return 0.0

    return pvariance(values)


def _get_next_roll_counts(
    states: Counter[GameState],
) -> Counter[int]:
    """
    Build weighted counts for every possible next roll.

    Each state is weighted by the number of observed roll paths that
    lead to it, while each individual roll within that state is weighted
    by the number of face combinations that produce that roll.
    """
    next_rolls_count: Counter[int] = Counter()

    for state, state_count in states.items():
        roll_counts: Counter[int] = Counter(
            sum(faces) for faces in product(*state.dice)
        )

        for roll, roll_count in roll_counts.items():
            next_rolls_count[roll] += roll_count * state_count

    return next_rolls_count


def _normalize_counts(counts: Counter[int]) -> dict[int, float]:
    """Convert weighted counts into probabilities."""
    total = sum(counts.values())

    if total == 0:
        return {}

    return {value: count / total for value, count in counts.items()}


def get_guess_evs(
    possible_rolls: dict[int, float],
    allowed_guesses: tuple[int, ...],
) -> dict[int, float]:
    """
    Calculate the expected payout of every possible guess.

    Returns a mapping of:
        guess -> expected payout
    """
    return {
        guess: sum(
            calc_payout(roll, guess) * probability
            for roll, probability in possible_rolls.items()
        )
        for guess in allowed_guesses
    }


def get_ev(
    possible_rolls: dict[int, float],
    allowed_guesses: tuple[int, ...],
) -> tuple[float, int]:
    """
    Backwards-compatible helper returning only the best EV and guess.
    """
    guess_evs = get_guess_evs(possible_rolls, allowed_guesses)
    best_guess = max(guess_evs, key=guess_evs.get) if guess_evs else None

    return guess_evs[best_guess], best_guess


def build_history_metrics(num_dice: int, num_sides: int) -> list[dict]:
    initial_state = create_initial_state(num_dice, num_sides)
    state_graph, _ = build_state_graph(initial_state)
    analysis: GraphAnalysis = analyze_state_graph(initial_state, state_graph)

    possible_guesses = tuple(range(num_dice, num_dice * num_sides + 1))

    rows = []

    for history in analysis.histories:
        depth = len(history)
        states = analysis.states_by_history[depth][history]

        state_counts = tuple(states.values())
        state_total = sum(state_counts)

        state_probabilities = tuple(count / state_total for count in state_counts)

        state_variances = tuple(
            _safe_variance(tuple(face for die in state.dice for face in die))
            for state in states
        )

        next_rolls_count = _get_next_roll_counts(states)
        next_rolls_probability = _normalize_counts(next_rolls_count)

        next_roll_entropy = entropy(
            list(next_rolls_probability.values()),
            base=2,
        )

        guess_evs = get_guess_evs(
            next_rolls_probability,
            possible_guesses,
        )

        sorted_evs = sorted(
            guess_evs.values(),
            reverse=True,
        )

        best_ev = sorted_evs[0]
        second_best_ev = sorted_evs[1] if len(sorted_evs) > 1 else best_ev

        best_guess = (
            max(
                guess_evs,
                key=guess_evs.get,
            )
            if guess_evs
            else None
        )

        ev_margin = best_ev - second_best_ev
        ev_variance = _safe_pvariance(tuple(guess_evs.values()))

        state_entropy = entropy(
            state_probabilities,
            base=2,
        )

        row = {
            "history": history,
            "num_dice": num_dice,
            "num_sides": num_sides,
            "depth": depth,
            "probability_in_depth": analysis.history_probabilities[depth][history],
            "states": states,
            # State uncertainty
            "num_states": len(states),
            "entropy": state_entropy,
            "effective_state_count": 2**state_entropy,
            "state_probabilities": sorted(state_probabilities),
            "state_probability_variance": _safe_variance(state_probabilities),
            # State structure
            "mean_state_remaining_faces_variance": mean(state_variances),
            "weighted_state_remaining_faces_variance": _weighted_mean(
                state_variances,
                state_probabilities,
            ),
            # Next-roll prediction
            "next_rolls_count": dict(next_rolls_count),
            "next_rolls_probability": next_rolls_probability,
            "next_roll_entropy": next_roll_entropy,
            "next_roll_max_probability": max(next_rolls_probability.values())
            if next_rolls_probability.values()
            else 0,
            "most_likely_roll": max(
                next_rolls_probability,
                key=next_rolls_probability.get,
            )
            if next_rolls_probability
            else None,
            # Guess / decision quality
            "expected_value": best_ev,
            "best_guess": best_guess,
            "ev_distribution": guess_evs,
            "ev_variance": ev_variance,
            "ev_margin": ev_margin,
            "normalized_ev_margin": ev_margin / (sorted_evs[0] - sorted_evs[-1])
            if sorted_evs[0] != sorted_evs[-1]
            else 0.0,
            "best_guess_payout_variance": variance(
                [
                    calc_payout(best_guess, roll)
                    * (next_rolls_probability[roll] - best_ev) ** 2
                    for roll in _get_next_roll_counts(states)
                ]
            )
            if len(_get_next_roll_counts(states)) > 2
            else 0,
        }
        rows.append(row)
    return rows


def build_all_history_metrics(
    num_dice_range: Iterable,
    num_sides_range: Iterable,
    return_as_list: bool = False,
    exclude: Iterable[tuple] = (),
) -> DataFrame | list[DataFrame]:
    """Builds a full list of all possible histories for all provided sides and number of dice configurations.
    Note that large values for number of dice and number of sides can result in the program hanging"""
    all_rows = []
    for num_dice, num_sides in product(num_dice_range, num_sides_range):
        if (num_dice, num_sides) not in exclude:
            print(
                f"START building history metrics for {num_sides} sides and {num_dice} dice."
            )
            if return_as_list:
                all_rows.append(DataFrame(build_history_metrics(num_dice, num_sides)))
            else:
                all_rows.extend(build_history_metrics(num_dice, num_sides))
            print(
                f"FINISH Building history metrics for {num_sides} sides and {num_dice} dice."
            )
    if return_as_list:
        return all_rows
    else:
        return DataFrame(all_rows)
