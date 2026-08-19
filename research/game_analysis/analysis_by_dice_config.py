from statistics import mean, median, pvariance, variance

import pandas as pd
from scipy.stats import median_abs_deviation


# =======================================================================
# Math & Statistical Helpers (Unchanged)
# =======================================================================
def _safe_variance(values: tuple[float, ...]) -> float:
    if len(values) < 2:
        return 0.0
    return variance(values)


def _safe_pvariance(values: tuple[float, ...]) -> float:
    if len(values) < 2:
        return 0.0
    return pvariance(values)


def _weighted_mean(values: list[float], weights: list[float]) -> float:
    if not values or sum(weights) == 0:
        return 0.0
    return sum(value * weight for value, weight in zip(values, weights)) / sum(weights)


def _weighted_median(values: list[float], weights: list[float]) -> float:
    if not values or sum(weights) == 0:
        return 0.0
    sorted_pairs = sorted(zip(values, weights), key=lambda pair: pair[0])
    total_weight = sum(weights)
    cumulative_weight = 0.0
    for value, weight in sorted_pairs:
        cumulative_weight += weight
        if cumulative_weight >= total_weight / 2:
            return value
    return sorted_pairs[-1][0]


def _weighted_variance(
    values: list[float], weights: list[float], w_mean: float
) -> float:
    if not values or sum(weights) == 0:
        return 0.0
    total_weight = sum(weights)
    return (
        sum(weight * (value - w_mean) ** 2 for value, weight in zip(values, weights))
        / total_weight
    )


def _weighted_mad(
    values: list[float], weights: list[float], median_value: float
) -> float:
    if not values:
        return 0.0
    deviations = [abs(value - median_value) for value in values]
    return _weighted_median(deviations, weights)


def _aggregate_metric(prefix: str, values: list[float], weights: list[float]) -> dict:
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
            values, weights, weighted_mean_value
        ),
        f"weighted_mad_{prefix}": _weighted_mad(values, weights, weighted_median_value),
    }


# =======================================================================
# Core Computation from History DataFrame
# =======================================================================
def generate_metrics(history_df: pd.DataFrame) -> pd.DataFrame:
    """Generate a DataFrame of game metrics aggregated by depth from a history DataFrame."""
    rows = []

    # Ensure sequential depth processing for information gain
    history_df = history_df.sort_values(by=["num_dice", "num_sides", "depth"])

    # Group by game configuration
    for (num_dice, num_sides), config_group in history_df.groupby(
        ["num_dice", "num_sides"]
    ):
        prev_mean_entropy = 0.0
        prev_weighted_mean_entropy = 0.0

        # Group by depth within the configuration
        for depth, group in config_group.groupby("depth"):
            weights = group["probability_in_depth"].tolist()

            # Derived variables that need light transformation from history columns
            max_entropy = group["entropy"].max()
            norm_entropies = (
                (group["entropy"] / max_entropy).fillna(0.0).tolist()
                if max_entropy > 0
                else [0.0] * len(group)
            )

            # Extract top state probability (last item in sorted probabilities list)
            top_state_probs = (
                group["state_probabilities"]
                .apply(lambda x: x[-1] if x else 0.0)
                .tolist()
            )

            # Effective next rolls based on entropy
            effective_next_rolls = (2 ** group["next_roll_entropy"]).tolist()

            # Initialize depth row
            aggregated_history_metrics = {
                "num_dice": num_dice,
                "num_sides": num_sides,
                "depth": depth,
                "num_histories": len(group),
                "num_states": sum(group["num_states"]),
            }

            # Metrics to aggregate: (prefix, values)
            metrics_to_agg = [
                ("states", group["num_states"].tolist()),
                ("entropy", group["entropy"].tolist()),
                ("effective_states", group["effective_state_count"].tolist()),
                ("norm_entropy", norm_entropies),
                ("top_state_prob", top_state_probs),
                ("state_prob_variance", group["state_probability_variance"].tolist()),
                (
                    "mean_state_remaining_faces_variance",
                    group["mean_state_remaining_faces_variance"].tolist(),
                ),
                (
                    "weighted_state_remaining_faces_variance",
                    group["weighted_state_remaining_faces_variance"].tolist(),
                ),
                ("next_roll_entropy", group["next_roll_entropy"].tolist()),
                ("effective_next_rolls", effective_next_rolls),
                (
                    "next_roll_max_probability",
                    group["next_roll_max_probability"].tolist(),
                ),
                ("expected_value", group["expected_value"].tolist()),
                ("ev_variance", group["ev_variance"].tolist()),
                ("ev_margin", group["ev_margin"].tolist()),
                ("normalized_ev_margin", group["normalized_ev_margin"].tolist()),
                (
                    "best_guess_payout_variance",
                    group["best_guess_payout_variance"].tolist(),
                ),
            ]

            # Apply aggregations
            for prefix, values in metrics_to_agg:
                aggregated_history_metrics.update(
                    _aggregate_metric(prefix, values, weights)
                )

            # Calculate Information Gain
            if depth > 0:
                aggregated_history_metrics["mean_information_gain"] = (
                    prev_mean_entropy - aggregated_history_metrics["mean_entropy"]
                )
                aggregated_history_metrics["weighted_mean_information_gain"] = (
                    prev_weighted_mean_entropy
                    - aggregated_history_metrics["weighted_mean_entropy"]
                )
            else:
                aggregated_history_metrics["mean_information_gain"] = 0.0
                aggregated_history_metrics["weighted_mean_information_gain"] = 0.0

            # Store current entropies for the next depth's information gain
            prev_mean_entropy = aggregated_history_metrics["mean_entropy"]
            prev_weighted_mean_entropy = aggregated_history_metrics[
                "weighted_mean_entropy"
            ]

            rows.append(aggregated_history_metrics)

    return pd.DataFrame(rows)
