# any graphs that compare different algorithms
import pandas as pd
from graph_config import AGENT_COMPARIONS_FIG_DIR, ALGORITHMS
from graph_utils import save_bar

GRAPHS = [
    ("average_payout", "Average Payout Per Algorithm", "Average Payout"),
    ("median_payout", "Median Payout Per Algorithm", "Median Payout"),
    (
        "standard_deviation_payout",
        "Standard Deviation of Payout per Algorithm",
        "Standard Deviation of Payout",
    ),
    ("minimum_payout", "Minimum Payout Per Algorithm", "Minimum Payout"),
    ("maximum_payout", "Maximum Payout Per Algorithm", "Maximum Payout"),
    ("exact_hit_rate", "Exact Hit Rate Per Algorithm", "Exact Hit Rate"),
    ("mean_absolute_error", "Mean Absolute Error Per Algorithm", "Mean Absolute Error"),
    (
        "average_operations",
        "Average Operation Count Per Algorithm",
        "Average Operation Count",
    ),
    (
        "maximum_operations",
        "Maximum Operation Count Per Algorithm",
        "Maximum Operation Count",
    ),
]

rows = []

for algorithm in ALGORITHMS:
    df = pd.read_csv(
        f"/Users/jamesekern/pythonProjects/gamblint/research/data/metric_tables/{algorithm}/{algorithm}.csv"
    )
    rows.append(
        {
            "algorithm": algorithm,
            **{metric: df.loc[0, metric] for metric, _, _ in GRAPHS},
        }
    )

constant_df = pd.DataFrame(rows).sort_values("algorithm")

for metric, title, ylabel in GRAPHS:
    save_bar(
        constant_df,
        x="algorithm",
        y=metric,
        output_path=f"{AGENT_COMPARIONS_FIG_DIR}/overall/overall_{metric}.png",
        title=title,
        x_label="Algorithm",
        y_label=ylabel,
    )
