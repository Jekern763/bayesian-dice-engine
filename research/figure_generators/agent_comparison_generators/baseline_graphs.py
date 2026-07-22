# graphs for baseline constant algorithms, 2-12
import pandas as pd
from graph_config import AGENT_COMPARIONS_FIG_DIR, CONSTANT_ALGORITHMS
from graph_utils import save_line

GRAPHS = [
    (
        "average_payout",
        "Average Payout for Constant Guess",
        "Average Payout",
    ),
    (
        "exact_hit_rate",
        "Exact Hit Rate for Constant Guess",
        "Exact Hit Rate",
    ),
    (
        "mean_absolute_error",
        "Mean Absolute Error for Constant Guess",
        "Mean Absolute Error",
    ),
    ("maximum_payout", "Maximum Payout for Constant Guess", "Maximum Payout"),
    ("median_payout", "Median Payout for Constant Guess", "Median Payout"),
]

rows = []

for algorithm in CONSTANT_ALGORITHMS:
    df = pd.read_csv(
        f"/Users/jamesekern/pythonProjects/gamblint/research/data/metric_tables/{algorithm}/{algorithm}.csv"
    )

    rows.append(
        {
            "constant": int(algorithm.replace("constant_agent_", "")),
            **{metric: df.loc[0, metric] for metric, _, _ in GRAPHS},
        }
    )

constant_df = pd.DataFrame(rows).sort_values("constant")

for metric, title, ylabel in GRAPHS:
    save_line(
        constant_df,
        x="constant",
        y=metric,
        output_path=f"{AGENT_COMPARIONS_FIG_DIR}/baseline_{metric}.png",
        title=title,
        x_label="Constant Guess",
        y_label=ylabel,
    )
