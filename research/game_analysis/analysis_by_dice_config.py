from statistics import mean, median

import pandas as pd
from scipy.stats import entropy, median_abs_deviation
from state_analysis import GraphAnalysis, analyze_state_graph
from state_graph import build_state_graph, create_initial_state


def _weighted_mean(values: list[float], weights: list[float]) -> float:
    """Calculate the weighted mean of a list of values."""
    if not values:
        return 0.0

    total_weight = sum(weights)

    if total_weight == 0:
        return 0.0

    return sum(value * weight for value, weight in zip(values, weights)) / total_weight


def _weighted_median(values: list[float], weights: list[float]) -> float:
    """Calculate the weighted median of a list of values."""
    if not values:
        return 0.0

    sorted_pairs = sorted(zip(values, weights), key=lambda pair: pair[0])
    total_weight = sum(weights)

    if total_weight == 0:
        return 0.0

    cumulative_weight = 0.0

    for value, weight in sorted_pairs:
        cumulative_weight += weight

        if cumulative_weight >= total_weight / 2:
            return value

    return sorted_pairs[-1][0]


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


def _compute_basic_depth_metrics(
    num_dice: int,
    num_sides: int,
    depth: int,
    states_by_depth: dict,
    analysis: GraphAnalysis,
) -> dict:
    """Compute metrics for a single depth level."""

    histories = list(analysis.histories_by_depth[depth])

    state_dists = [analysis.states_by_history[depth][history] for history in histories]

    history_probs = list(analysis.history_probabilities[depth].values())

    # ------------------------------------------------------------
    # State distributions
    # ------------------------------------------------------------

    lengths = [len(dist) for dist in state_dists]

    entropies = [entropy(list(dist.values()), base=2) for dist in state_dists]

    # ------------------------------------------------------------
    # Previous-depth metrics
    # ------------------------------------------------------------

    if depth > 0:
        past_histories = list(analysis.histories_by_depth[depth - 1])

        past_state_dists = [
            analysis.states_by_history[depth - 1][history] for history in past_histories
        ]

        past_history_probs = list(analysis.history_probabilities[depth - 1].values())

        past_entropies = [
            entropy(list(dist.values()), base=2) for dist in past_state_dists
        ]
    else:
        past_entropies = []
        past_history_probs = []

    # ------------------------------------------------------------
    # Normalized entropy
    # ------------------------------------------------------------

    max_entropy = max(entropies, default=0.0)

    norm_entropies = [
        entropy_value / max_entropy if max_entropy > 0 else 0.0
        for entropy_value in entropies
    ]

    # ------------------------------------------------------------
    # Top-state probability
    # ------------------------------------------------------------

    top_state_probs = [
        max(dist.values()) / sum(dist.values())
        if dist and sum(dist.values()) > 0
        else 0.0
        for dist in state_dists
    ]

    # ------------------------------------------------------------
    # Weighted medians
    # ------------------------------------------------------------

    weighted_median_states = _weighted_median(
        lengths,
        history_probs,
    )

    weighted_median_entropy = _weighted_median(
        entropies,
        history_probs,
    )

    weighted_median_norm_entropy = _weighted_median(
        norm_entropies,
        history_probs,
    )

    weighted_median_top_state_prob = _weighted_median(
        top_state_probs,
        history_probs,
    )

    # ------------------------------------------------------------
    # Basic metrics
    # ------------------------------------------------------------

    basic_rows = {
        "num_dice": num_dice,
        "num_sides": num_sides,
        "depth": depth,
        "num_histories": len(histories),
        "num_states": len(states_by_depth[depth]),
        # ========================================================
        # Unweighted State Metrics
        # ========================================================
        "mean_states": mean(lengths) if lengths else 0.0,
        "median_states": median(lengths) if lengths else 0.0,
        "min_states": min(lengths) if lengths else 0,
        "max_states": max(lengths) if lengths else 0,
        "mad_states": (median_abs_deviation(lengths) if lengths else 0.0),
        # ========================================================
        # Unweighted Entropy Metrics
        # ========================================================
        "mean_entropy": mean(entropies) if entropies else 0.0,
        "median_entropy": median(entropies) if entropies else 0.0,
        "min_entropy": min(entropies) if entropies else 0.0,
        "max_entropy": max(entropies) if entropies else 0.0,
        "mad_entropy": (median_abs_deviation(entropies) if entropies else 0.0),
        "mean_effective_states": 2 ** mean(entropies),
        "median_effective_states": 2 ** median(entropies),
        # ========================================================
        # Unweighted Normalized Entropy
        # ========================================================
        "mean_norm_entropy": (mean(norm_entropies) if norm_entropies else 0.0),
        "median_norm_entropy": (median(norm_entropies) if norm_entropies else 0.0),
        "min_norm_entropy": (min(norm_entropies) if norm_entropies else 0.0),
        "max_norm_entropy": (max(norm_entropies) if norm_entropies else 0.0),
        "mad_norm_entropy": (
            median_abs_deviation(norm_entropies) if norm_entropies else 0.0
        ),
        # ========================================================
        # Unweighted Top-State Metrics
        # ========================================================
        "mean_top_state_prob": (mean(top_state_probs) if top_state_probs else 0.0),
        "median_top_state_prob": (median(top_state_probs) if top_state_probs else 0.0),
        "min_top_state_prob": (min(top_state_probs) if top_state_probs else 0.0),
        "max_top_state_prob": (max(top_state_probs) if top_state_probs else 0.0),
        "mad_top_state_prob": (
            median_abs_deviation(top_state_probs) if top_state_probs else 0.0
        ),
        # ========================================================
        # Weighted State Metrics
        # ========================================================
        "weighted_mean_states": _weighted_mean(
            lengths,
            history_probs,
        ),
        "weighted_median_states": weighted_median_states,
        "weighted_mad_states": _weighted_mad(
            lengths,
            history_probs,
            weighted_median_states,
        ),
        # ========================================================
        # Weighted Entropy Metrics
        # ========================================================
        "weighted_mean_entropy": _weighted_mean(
            entropies,
            history_probs,
        ),
        "weighted_median_entropy": weighted_median_entropy,
        "weighted_mad_entropy": _weighted_mad(
            entropies,
            history_probs,
            weighted_median_entropy,
        ),
        "weighted_mean_effective_states": 2 ^ _weighted_mean(entropies, history_probs),
        "weighted_median_effective_states": 2 ^ weighted_median_entropy,
        # ========================================================
        # Weighted Normalized Entropy
        # ========================================================
        "weighted_mean_norm_entropy": _weighted_mean(
            norm_entropies,
            history_probs,
        ),
        "weighted_median_norm_entropy": weighted_median_norm_entropy,
        "weighted_mad_norm_entropy": _weighted_mad(
            norm_entropies,
            history_probs,
            weighted_median_norm_entropy,
        ),
        # ========================================================
        # Weighted Top-State Metrics
        # ========================================================
        "weighted_mean_top_state_prob": _weighted_mean(
            top_state_probs,
            history_probs,
        ),
        "weighted_median_top_state_prob": weighted_median_top_state_prob,
        "weighted_mad_top_state_prob": _weighted_mad(
            top_state_probs,
            history_probs,
            weighted_median_top_state_prob,
        ),
        # ========================================================
        # State Variance Metrics
        # ========================================================
    }

    # ------------------------------------------------------------
    # Advanced metrics
    # ------------------------------------------------------------

    if depth > 0:
        average_information_gain = mean(past_entropies) - basic_rows["mean_entropy"]

        weighted_average_information_gain = (
            _weighted_mean(
                past_entropies,
                past_history_probs,
            )
            - basic_rows["weighted_mean_entropy"]
        )
    else:
        average_information_gain = 0.0
        weighted_average_information_gain = 0.0

    advanced_rows = {
        "average_information_gain": average_information_gain,
        "weighted_average_information_gain": (weighted_average_information_gain),
    }

    return basic_rows | advanced_rows


def generate_metrics(
    dice_num_values: list[int],
    side_num_values: list[int],
) -> pd.DataFrame:
    """Generate a DataFrame of game metrics."""

    rows = []

    for num_dice in dice_num_values:
        for num_sides in side_num_values:
            initial = create_initial_state(
                num_dice,
                num_sides,
            )

            graph, states_by_depth = build_state_graph(initial)

            analysis = analyze_state_graph(
                initial,
                graph,
            )

            for depth in analysis.histories_by_depth:
                rows.append(
                    _compute_basic_depth_metrics(
                        num_dice,
                        num_sides,
                        depth,
                        states_by_depth,
                        analysis,
                    )
                )

    return pd.DataFrame(rows)
