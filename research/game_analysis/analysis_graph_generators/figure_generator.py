import graph_utils
from config import get_dataframes

history_df, config_df = get_dataframes()

history_df_2d6 = history_df[
    (history_df["num_dice"] == 2) & (history_df["num_sides"] == 6)
]
config_df_2d6 = config_df[(config_df["num_dice"] == 2) & (config_df["num_sides"] == 6)]

OUTPUT_DIR = "/Users/jamesekern/pythonProjects/gamblint/research/figures/game_analysis"

# ========== Metrics by Depth ==========

metrics_to_graph = [
    "num_states",
    "median_states",
    "weighted_median_states",
    "weighted_variance_states",
    "weighted_median_entropy",
    "weighted_median_effective_states",
    "weighted_mean_state_prob_variance",
    "weighted_mean_next_roll_entropy",
    "weighted_mean_next_roll_max_probability",
    "weighted_median_expected_value",
    "weighted_mean_ev_variance",
    "weighted_mean_ev_margin",
    "weighted_mean_normalized_ev_margin",
    "weighted_mean_best_guess_payout_variance",
]

for metric in metrics_to_graph:
    graph_utils.save_line(
        df=config_df_2d6,
        x="depth",
        y=metric,
        title=f"{metric} vs depth",
        x_label="depth",
        y_label=metric,
        output_path=f"{OUTPUT_DIR}/{metric}_vs_depth.png",
    )
# ========== Metrics by Number of Possible States ==========

metrics_to_graph = [
    "entropy",
    "next_roll_max_probability",
    "expected_value",
    "most_likely_roll",
]

for metric in metrics_to_graph:
    avg_by_states = history_df_2d6.groupby("num_states", as_index=False)[metric].mean()

    graph_utils.save_line(
        df=avg_by_states,
        x="num_states",
        y=metric,
        title=f"Average {metric} vs Number of States",
        x_label="num_states",
        y_label=metric,
        output_path=f"{OUTPUT_DIR}/{metric}_vs_num_states.png",
    )

# ========== Metrics by Entropy ==========

metrics_to_graph = [
    "num_states",
    "ev_variance",
    "next_roll_max_probability",
    "expected_value",
    "most_likely_roll",
    "state_probability_variance",
    "best_guess",
]

for metric in metrics_to_graph:
    avg_by_entropy = history_df_2d6.groupby("entropy", as_index=False)[metric].mean()
    graph_utils.save_line(
        df=avg_by_entropy,
        x="entropy",
        y=metric,
        title=f"{metric} vs Entropy",
        x_label="Entropy",
        y_label=metric,
        output_path=f"{OUTPUT_DIR}/{metric}_vs_entropy.png",
    )
