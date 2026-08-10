import math
from statistics import mean, median

import pandas as pd
from scipy.stats import entropy, median_abs_deviation
from state_analysis import GraphAnalysis, analyze_state_graph
from state_graph import build_state_graph, create_initial_state


def _weighted_mean(values: list[float], weights: list[float]) -> float:
    """Calculates the weighted mean of a list of values."""
    total_weight = sum(weights)
    if not total_weight:
        return 0.0
    return sum(v * w for v, w in zip(values, weights)) / total_weight


def _weighted_median(values: list[float], weights: list[float]) -> float:
    """Calculates the weighted median of a list of values."""
    if not values:
        return 0.0

    sorted_pairs = sorted(zip(values, weights), key=lambda x: x[0])
    total_weight = sum(weights)
    cumulative_weight = 0.0

    for value, weight in sorted_pairs:
        cumulative_weight += weight
        if cumulative_weight >= total_weight / 2.0:
            return value

    return sorted_pairs[-1][0]


def _weighted_mad(
    values: list[float], weights: list[float], median_val: float
) -> float:
    """Calculates the weighted median absolute deviation (MAD)."""
    if not values:
        return 0.0
    deviations = [abs(v - median_val) for v in values]
    return _weighted_median(deviations, weights)


def _compute_basic_depth_metrics(
    num_dice: int,
    num_sides: int,
    depth: int,
    states_by_depth: dict,
    analysis: GraphAnalysis,
) -> dict:
    """Computes all unweighted and weighted metrics for a single depth level."""
    histories = list(analysis.histories_by_depth[depth])

    # Probability distributions and probabilities for each history
    state_dists = [analysis.states_by_history[depth][h] for h in histories]
    probs = [analysis.history_probabilities[depth][h] for h in histories]

    # Core lists
    lengths = [len(dist) for dist in state_dists]
    entropies = [entropy(list(dist.values()), base=2) for dist in state_dists]

    # Calculate normalized entropies
    max_entropies = [math.log2(length) if length > 1 else 0.0 for length in lengths]
    norm_entropies = [
        e / me if me > 0 else 0.0 for e, me in zip(entropies, max_entropies)
    ]

    # Probability of the single most likely remaining state (top state)
    top_state_probs = [
        max(dist.values()) / sum(dist.values())
        if dist and sum(dist.values()) > 0
        else 0.0
        for dist in state_dists
    ]

    # Pre-calculate weighted medians for MAD functions
    wt_median_entropy = _weighted_median(entropies, probs)
    wt_median_norm_entropy = _weighted_median(norm_entropies, probs)

    return {
        "num_dice": num_dice,
        "num_sides": num_sides,
        "depth": depth,
        "num_histories": len(histories),
        "num_states": len(states_by_depth[depth]),
        # ==================================================
        # Basic Unweighted Metrics
        # ==================================================
        "mean_states": mean(lengths) if lengths else 0.0,
        "median_states": median(lengths),
        "min_states": min(lengths) if lengths else 0,
        "max_states": max(lengths) if lengths else 0,
        "mad_states": median_abs_deviation(lengths),
        "mean_entropy": mean(entropies) if entropies else 0.0,
        "max_entropy": max(entropies),
        "min_entropy": min(entropies),
        "median_entropy": median(entropies) if entropies else 0.0,
        "mad_entropy": median_abs_deviation(entropies) if entropies else 0.0,
        # ==================================================
        # Unweighted Normalized Entropy
        # ==================================================
        "mean_norm_entropy": mean(norm_entropies) if norm_entropies else 0.0,
        "median_norm_entropy": median(norm_entropies) if norm_entropies else 0.0,
        "min_norm_entropy": min(norm_entropies),
        "max_norm_entropy": max(norm_entropies),
        "mad_norm_entropy": median_abs_deviation(norm_entropies),
        # ==================================================
        # Unweighted Top-State Metrics
        # ==================================================
        "mean_top_state_prob": mean(top_state_probs) if top_state_probs else 0.0,
        "median_top_state_prob": median(top_state_probs) if top_state_probs else 0.0,
        "min_top_state_prob": min(top_state_probs),
        "max_top_state_prob": max(top_state_probs),
        "mad_top_state_prob": median_abs_deviation(top_state_probs),
        # ==================================================
        # Weighted Basic Metrics
        # ==================================================
        "weighted_mean_states": _weighted_mean(lengths, probs),
        "weighted_median_states": _weighted_median(lengths, probs),
        "weighted_mad_states": _weighted_mad(
            lengths, probs, _weighted_median(lengths, probs)
        ),
        "weighted_mean_entropy": _weighted_mean(entropies, probs),
        "weighted_median_entropy": wt_median_entropy,
        "weighted_mad_entropy": _weighted_mad(entropies, probs, wt_median_entropy),
        # ==================================================
        # Weighted Normalized Entropy
        # ==================================================
        "weighted_mean_norm_entropy": _weighted_mean(norm_entropies, probs),
        "weighted_median_norm_entropy": wt_median_norm_entropy,
        "weighted_mad_norm_entropy": _weighted_mad(
            norm_entropies, probs, wt_median_norm_entropy
        ),
        # ==================================================
        # Weighted Top-State Metrics
        # ==================================================
        "weighted_mean_top_state_prob": _weighted_mean(top_state_probs, probs),
        "weighted_median_top_state_prob": _weighted_median(top_state_probs, probs),
        "weighetd_mad_top_state_prob": _weighted_mad(
            top_state_probs, probs, _weighted_median(top_state_probs, probs)
        ),
    }


def generate_metrics(
    dice_num_values: range,
    side_num_values: range,
) -> pd.DataFrame:
    """Generates a DataFrame of game metrics across various dice and side configurations."""
    rows = []

    for num_dice in dice_num_values:
        for num_sides in side_num_values:
            initial = create_initial_state(num_dice, num_sides)

            graph, states_by_depth = build_state_graph(initial)
            analysis = analyze_state_graph(initial, graph)

            for depth in analysis.histories_by_depth:
                row_metrics = _compute_basic_depth_metrics(
                    num_dice, num_sides, depth, states_by_depth, analysis
                )
                rows.append(row_metrics)

    return pd.DataFrame(rows)
