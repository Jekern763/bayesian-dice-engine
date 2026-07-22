# any graphs that compare different algorithms
import pandas as pd
from graph_config import AGENT_COMPARIONS_FIG_DIR, ALGORITHM_DFS, ALGORITHMS
from graph_utils import save_bar, save_scatter

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

# a graph of derived average_payout/average_operations
rows = []
for algorithm, df in ALGORITHM_DFS.items():
    rows.append(
        {
            "algorithm": algorithm,
            "effeciency": df.loc[0, "average_payout"] / df.loc[0, "average_operations"],
        }
    )

derived_df = pd.DataFrame(rows).sort_values("algorithm")
save_bar(
    derived_df,
    x="algorithm",
    y="effeciency",
    output_path=f"{AGENT_COMPARIONS_FIG_DIR}/overall/overall_effeciency.png",
    title="Effeciency Per Algorithm",
    x_label="Algorithm",
    y_label="Effeciency (average_payout/average_operations)",
)

# ========== FINISHED WITH BASIC METRIC VS ALGORITHM GRAPHS. MOVING ON TO METRIC VS METRIC SCATTER PLOTS ==========

GRAPHS = [
    # Operations vs Performance
    ("average_operations", "average_payout", "Average Payout vs Average Operations"),
    ("average_operations", "exact_hit_rate", "Exact Hit Rate vs Average Operations"),
    ("average_operations", "mean_absolute_error", "MAE vs Average Operations"),
    # Performance vs Performance
    ("exact_hit_rate", "average_payout", "Average Payout vs Exact Hit Rate"),
    ("mean_absolute_error", "average_payout", "Average Payout vs MAE"),
    ("mean_absolute_error", "exact_hit_rate", "Exact Hit Rate vs MAE"),
    # Risk vs Performance (if available)
    (
        "standard_deviation_payout",
        "average_payout",
        "Average Payout vs Payout Variability",
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
            **{metric: df.loc[0, metric] for _, metric, _ in GRAPHS},
        }
    )
for metric_x, metric_y, title in GRAPHS:
    save_scatter(
        pd.DataFrame(rows).sort_values("algorithm"),
        x=metric_x,
        y=metric_y,
        label="algorithm",
        title=title,
        x_label=metric_x.replace("_", " ").title(),
        y_label=metric_y.replace("_", " ").title(),
        output_path=f"{AGENT_COMPARIONS_FIG_DIR}/overall/{metric_x}_vs_{metric_y}.png",
        x_axis_type="log" if "operation" in metric_x else "-",
        y_axis_type="log" if "operation" in metric_y else "-",
        textposition="bottom left" if metric_x == "exact_hit_rate" else "top right",
    )
