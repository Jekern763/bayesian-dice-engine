import sys
from collections import Counter
from itertools import product
from pathlib import Path
from statistics import mean, median, pvariance, variance

import pandas as pd
from scipy.stats import entropy, median_abs_deviation
from state_analysis import GameState, GraphAnalysis, analyze_state_graph
from state_graph import build_state_graph, create_initial_state

# =======================================================================
# Game Engine Setup
# =======================================================================
game_engine_dir = Path(
    "/Users/jamesekern/pythonProjects/gamblint/backend/game_engine"
).resolve()

module_dir = game_engine_dir.parent

if str(game_engine_dir) not in sys.path:
    sys.path.append(str(game_engine_dir))

if str(module_dir) not in sys.path:
    sys.path.insert(0, str(module_dir))

from game import Game  # type: ignore


# =======================================================================
# Math & Statistical Helpers
# =======================================================================
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


def _weighted_mean(values: list[float], weights: list[float]) -> float:
    """Calculate the weighted mean of a list of values."""
    if not values or sum(weights) == 0:
        return 0.0

    return sum(value * weight for value, weight in zip(values, weights)) / sum(weights)


def _weighted_median(
    values: list[float],
    weights: list[float],
) -> float:
    """Calculate the weighted median of a list of values."""
    if not values or sum(weights) == 0:
        return 0.0

    sorted_pairs = sorted(
        zip(values, weights),
        key=lambda pair: pair[0],
    )

    total_weight = sum(weights)
    cumulative_weight = 0.0

    for value, weight in sorted_pairs:
        cumulative_weight += weight

        if cumulative_weight >= total_weight / 2:
            return value

    return sorted_pairs[-1][0]


def _weighted_variance(
    values: list[float],
    weights: list[float],
    w_mean: float,
) -> float:
    """Calculate the weighted population variance."""
    if not values or sum(weights) == 0:
        return 0.0

    total_weight = sum(weights)

    return (
        sum(weight * (value - w_mean) ** 2 for value, weight in zip(values, weights))
        / total_weight
    )


def _weighted_mad(
    values: list[float],
    weights: list[float],
    median_value: float,
) -> float:
    """Calculate the weighted median absolute deviation."""
    if not values:
        return 0.0

    deviations = [abs(value - median_value) for value in values]

    return _weighted_median(deviations, weights)


def _aggregate_metric(
    prefix: str,
    values: list[float],
    weights: list[float],
) -> dict:
    """
    Generate standard and weighted statistical aggregations
    for a metric measured across histories.
    """
    if not values:
        return {
            f"mean_{prefix}": 0.0,
            f"median_{prefix}": 0.0,
            f"min_{prefix}": 0.0,
            f"max_{prefix}": 0.0,
            f"variance_{prefix}": 0.0,
            f"mad_{prefix}": 0.0,
            f"weighted_mean_{prefix}": 0.0,
            f"weighted_median_{prefix}": 0.0,
            f"weighted_variance_{prefix}": 0.0,
            f"weighted_mad_{prefix}": 0.0,
        }

    median_value = median(values)
    weighted_mean_value = _weighted_mean(values, weights)
    weighted_median_value = _weighted_median(values, weights)

    return {
        f"mean_{prefix}": mean(values),
        f"median_{prefix}": median_value,
        f"min_{prefix}": min(values),
        f"max_{prefix}": max(values),
        f"variance_{prefix}": _safe_variance(tuple(values)),
        f"mad_{prefix}": median_abs_deviation(values),
        f"weighted_mean_{prefix}": weighted_mean_value,
        f"weighted_median_{prefix}": weighted_median_value,
        f"weighted_variance_{prefix}": _weighted_variance(
            values,
            weights,
            weighted_mean_value,
        ),
        f"weighted_mad_{prefix}": _weighted_mad(
            values,
            weights,
            weighted_median_value,
        ),
    }


# =======================================================================
# Roll Prediction & EV Helpers
# =======================================================================
def _get_next_roll_counts(
    states: Counter[GameState],
) -> Counter[int]:
    """Build weighted counts for every possible next roll."""
    next_rolls_count: Counter[int] = Counter()

    for state, state_count in states.items():
        roll_counts: Counter[int] = Counter(
            sum(faces) for faces in product(*state.dice)
        )

        for roll, roll_count in roll_counts.items():
            next_rolls_count[roll] += roll_count * state_count

    return next_rolls_count


def _normalize_counts(
    counts: Counter[int],
) -> dict[int, float]:
    """Convert weighted counts into probabilities."""
    total = sum(counts.values())

    if total == 0:
        return {}

    return {value: count / total for value, count in counts.items()}


def get_guess_evs(
    possible_rolls: dict[int, float],
    allowed_guesses: tuple[int, ...],
    calc_payout_fn,
) -> dict[int, float]:
    """Calculate the expected payout of every possible guess."""
    return {
        guess: sum(
            calc_payout_fn(roll, guess) * probability
            for roll, probability in possible_rolls.items()
        )
        for guess in allowed_guesses
    }


# =======================================================================
# Core Computation
# =======================================================================
def _compute_basic_depth_metrics(
    num_dice: int,
    num_sides: int,
    depth: int,
    states_by_depth: dict,
    analysis: GraphAnalysis,
    calc_payout_fn,
) -> dict:
    """Compute metrics for a single depth level."""

    histories = list(analysis.histories_by_depth[depth])

    history_probs = [
        analysis.history_probabilities[depth][history] for history in histories
    ]

    possible_guesses = tuple(
        range(
            num_dice,
            num_dice * num_sides + 1,
        )
    )

    # ------------------------------------------------------------
    # Storage arrays for per-history metrics
    # ------------------------------------------------------------
    lengths = []
    entropies = []
    effective_states = []
    top_state_probs = []
    state_prob_variances = []

    mean_state_remaining_faces_variances = []
    weighted_state_remaining_faces_variances = []

    next_roll_entropies = []
    effective_next_rolls = []
    next_roll_max_probs = []

    expected_values = []
    ev_variances = []
    ev_margins = []
    normalized_ev_margins = []
    best_guess_payout_variances = []

    # ------------------------------------------------------------
    # Loop through each history to extract its metrics
    # ------------------------------------------------------------
    for history in histories:
        states = analysis.states_by_history[depth][history]

        state_counts = tuple(states.values())
        state_total = sum(state_counts)

        state_probabilities = tuple(count / state_total for count in state_counts)

        # --------------------------------------------------------
        # Basic State Information
        # --------------------------------------------------------
        lengths.append(len(states))

        st_entropy = entropy(
            state_probabilities,
            base=2,
        )

        entropies.append(st_entropy)

        # Effective number of states:
        #
        #     N_eff = 2^H
        #
        # This is calculated per history before aggregation so that
        # mean effective states != 2^(mean entropy).
        effective_states.append(2**st_entropy)

        top_state_probs.append(max(state_probabilities) if state_probabilities else 0.0)

        state_prob_variances.append(_safe_variance(state_probabilities))

        # --------------------------------------------------------
        # Remaining Faces Variance
        # --------------------------------------------------------
        state_variances = tuple(
            _safe_variance(tuple(face for die in state.dice for face in die))
            for state in states
        )

        mean_state_remaining_faces_variances.append(
            mean(state_variances) if state_variances else 0.0
        )

        weighted_state_remaining_faces_variances.append(
            _weighted_mean(
                list(state_variances),
                list(state_probabilities),
            )
            if state_variances
            else 0.0
        )

        # --------------------------------------------------------
        # Next Roll Predictions
        # --------------------------------------------------------
        next_rolls_count = _get_next_roll_counts(states)

        next_rolls_probability = _normalize_counts(next_rolls_count)

        next_roll_entropy = entropy(
            list(next_rolls_probability.values()),
            base=2,
        )

        next_roll_entropies.append(next_roll_entropy)

        # Effective number of next-roll outcomes:
        #
        #     N_eff = 2^H
        #
        effective_next_rolls.append(2**next_roll_entropy)

        next_roll_max_probs.append(
            max(next_rolls_probability.values()) if next_rolls_probability else 0.0
        )

        # --------------------------------------------------------
        # EV and Guess Distributions
        # --------------------------------------------------------
        guess_evs = get_guess_evs(
            next_rolls_probability,
            possible_guesses,
            calc_payout_fn,
        )

        if guess_evs:
            sorted_evs = sorted(
                guess_evs.values(),
                reverse=True,
            )

            best_ev = sorted_evs[0]

            second_best_ev = sorted_evs[1] if len(sorted_evs) > 1 else best_ev

            best_guess = max(
                guess_evs,
                key=guess_evs.get,
            )

            expected_values.append(best_ev)

            ev_variances.append(_safe_pvariance(tuple(guess_evs.values())))

            # Difference between the best and second-best guess.
            ev_margin = best_ev - second_best_ev

            ev_margins.append(ev_margin)

            # Difference between best and worst guess.
            range_evs = sorted_evs[0] - sorted_evs[-1]

            normalized_ev_margins.append(ev_margin / range_evs if range_evs else 0.0)

            # ----------------------------------------------------
            # Actual payout variance of the optimal guess
            #
            # Var(X) = sum P(r) * (X_r - E[X])^2
            # ----------------------------------------------------
            payout_variance = sum(
                probability * (calc_payout_fn(best_guess, roll) - best_ev) ** 2
                for roll, probability in next_rolls_probability.items()
            )

            best_guess_payout_variances.append(payout_variance)

        else:
            expected_values.append(0.0)
            ev_variances.append(0.0)
            ev_margins.append(0.0)
            normalized_ev_margins.append(0.0)
            best_guess_payout_variances.append(0.0)

    # ------------------------------------------------------------
    # Calculate Normalized Entropies
    # ------------------------------------------------------------
    max_entropy = max(
        entropies,
        default=0.0,
    )

    norm_entropies = [
        entropy_value / max_entropy if max_entropy > 0 else 0.0
        for entropy_value in entropies
    ]

    # ============================================================
    # 1. Metrics Originating from By-History Aggregations
    # ============================================================
    aggregated_history_metrics = {
        "num_dice": num_dice,
        "num_sides": num_sides,
        "depth": depth,
        "num_histories": len(histories),
        "num_states": len(states_by_depth[depth]),
    }

    # ------------------------------------------------------------
    # State Metrics
    # ------------------------------------------------------------
    aggregated_history_metrics.update(
        _aggregate_metric(
            "states",
            lengths,
            history_probs,
        )
    )

    aggregated_history_metrics.update(
        _aggregate_metric(
            "entropy",
            entropies,
            history_probs,
        )
    )

    aggregated_history_metrics.update(
        _aggregate_metric(
            "effective_states",
            effective_states,
            history_probs,
        )
    )

    aggregated_history_metrics.update(
        _aggregate_metric(
            "norm_entropy",
            norm_entropies,
            history_probs,
        )
    )

    aggregated_history_metrics.update(
        _aggregate_metric(
            "top_state_prob",
            top_state_probs,
            history_probs,
        )
    )

    aggregated_history_metrics.update(
        _aggregate_metric(
            "state_prob_variance",
            state_prob_variances,
            history_probs,
        )
    )

    aggregated_history_metrics.update(
        _aggregate_metric(
            "mean_state_remaining_faces_variance",
            mean_state_remaining_faces_variances,
            history_probs,
        )
    )

    aggregated_history_metrics.update(
        _aggregate_metric(
            "weighted_state_remaining_faces_variance",
            weighted_state_remaining_faces_variances,
            history_probs,
        )
    )

    # ------------------------------------------------------------
    # Next Roll Metrics
    # ------------------------------------------------------------
    aggregated_history_metrics.update(
        _aggregate_metric(
            "next_roll_entropy",
            next_roll_entropies,
            history_probs,
        )
    )

    aggregated_history_metrics.update(
        _aggregate_metric(
            "effective_next_rolls",
            effective_next_rolls,
            history_probs,
        )
    )

    aggregated_history_metrics.update(
        _aggregate_metric(
            "next_roll_max_probability",
            next_roll_max_probs,
            history_probs,
        )
    )

    # ------------------------------------------------------------
    # EV Metrics
    # ------------------------------------------------------------
    aggregated_history_metrics.update(
        _aggregate_metric(
            "expected_value",
            expected_values,
            history_probs,
        )
    )

    aggregated_history_metrics.update(
        _aggregate_metric(
            "ev_variance",
            ev_variances,
            history_probs,
        )
    )

    aggregated_history_metrics.update(
        _aggregate_metric(
            "ev_margin",
            ev_margins,
            history_probs,
        )
    )

    aggregated_history_metrics.update(
        _aggregate_metric(
            "normalized_ev_margin",
            normalized_ev_margins,
            history_probs,
        )
    )

    aggregated_history_metrics.update(
        _aggregate_metric(
            "best_guess_payout_variance",
            best_guess_payout_variances,
            history_probs,
        )
    )

    # ============================================================
    # 2. Derived / Advanced Non-History Metrics
    # ============================================================
    derived_metrics = {}

    # ------------------------------------------------------------
    # Information Gain
    # ------------------------------------------------------------
    if depth > 0:
        past_histories = list(analysis.histories_by_depth[depth - 1])

        past_history_probs = [
            analysis.history_probabilities[depth - 1][history]
            for history in past_histories
        ]

        past_entropies = [
            entropy(
                list(analysis.states_by_history[depth - 1][history].values()),
                base=2,
            )
            for history in past_histories
        ]

        derived_metrics["mean_information_gain"] = (
            mean(past_entropies) - aggregated_history_metrics["mean_entropy"]
            if past_entropies
            else 0.0
        )

        derived_metrics["weighted_mean_information_gain"] = (
            _weighted_mean(
                past_entropies,
                past_history_probs,
            )
            - aggregated_history_metrics["weighted_mean_entropy"]
            if past_entropies
            else 0.0
        )

    else:
        derived_metrics["mean_information_gain"] = 0.0
        derived_metrics["weighted_mean_information_gain"] = 0.0

    # ------------------------------------------------------------
    # Combine Both Sections
    # ------------------------------------------------------------
    return {
        **aggregated_history_metrics,
        **derived_metrics,
    }


# =======================================================================
# Public Metric Generator
# =======================================================================
def generate_metrics(
    dice_num_values: list[int],
    side_num_values: list[int],
) -> pd.DataFrame:
    """Generate a DataFrame of game metrics."""

    rows = []

    for num_dice in dice_num_values:
        for num_sides in side_num_values:
            # ----------------------------------------------------
            # Create game instance to retrieve payout function
            # ----------------------------------------------------
            game_instance = Game(
                num_dice,
                num_sides,
            )

            calc_payout_fn = game_instance.calc_payout

            # ----------------------------------------------------
            # Build state graph and analyze histories
            # ----------------------------------------------------
            initial = create_initial_state(
                num_dice,
                num_sides,
            )

            graph, states_by_depth = build_state_graph(initial)

            analysis = analyze_state_graph(
                initial,
                graph,
            )

            # ----------------------------------------------------
            # Generate one row per depth
            # ----------------------------------------------------
            for depth in analysis.histories_by_depth:
                rows.append(
                    _compute_basic_depth_metrics(
                        num_dice,
                        num_sides,
                        depth,
                        states_by_depth,
                        analysis,
                        calc_payout_fn,
                    )
                )

    return pd.DataFrame(rows)
