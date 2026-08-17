import numpy as np
import pandas as pd
import plotly.graph_objects as go
from analysis_by_history import build_all_history_metrics


def plot_correlation_matrix(
    corr: pd.DataFrame,
    title: str = "Correlation Matrix",
):
    fig = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.index,
            zmin=-1,
            zmax=1,
            text=corr.round(2).values,
            texttemplate="%{text}",
            hovertemplate=(
                "<b>%{y}</b><br><b>%{x}</b><br>Correlation: %{z:.4f}<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        title=title,
        width=1600,
        height=1600,
        xaxis={
            "side": "bottom",
            "tickangle": 45,
        },
        yaxis={
            "autorange": "reversed",
        },
    )

    return fig


def calculate_correlation_matrix(
    df: pd.DataFrame,
    method: str = "pearson",
) -> pd.DataFrame:
    """Calculate correlations between all numeric metrics."""

    numeric_df = df.select_dtypes(include="number")

    return numeric_df.corr(method=method)


def rank_correlations(
    corr: pd.DataFrame,
    min_strength: float = 0.60,
) -> pd.DataFrame:
    rows, cols = np.triu_indices_from(corr, k=1)

    ranked = pd.DataFrame(
        {
            "metric_1": corr.index[rows],
            "metric_2": corr.columns[cols],
            "correlation": corr.values[rows, cols],
        }
    )

    ranked["strength"] = ranked["correlation"].abs()

    return (
        ranked[ranked["strength"] >= min_strength]
        .sort_values("strength", ascending=False)
        .reset_index(drop=True)
    )


def plot_correlation_ranking(
    ranked: pd.DataFrame,
    title: str,
):
    display_df = ranked.copy()

    # Format for display
    display_df["correlation"] = display_df["correlation"].map(lambda x: f"{x:.3f}")
    display_df["strength"] = display_df["strength"].map(lambda x: f"{x:.3f}")

    fig = go.Figure(
        data=[
            go.Table(
                columnwidth=[300, 300, 120, 120],
                header={
                    "values": list(display_df.columns),
                    "align": "left",
                    "font": {"size": 14},
                    "height": 30,
                },
                cells={
                    "values": [display_df[col] for col in display_df.columns],
                    "align": "left",
                    "font": {"size": 12},
                    "height": 25,
                },
            )
        ]
    )

    fig.update_layout(
        title={
            "text": title,
            "x": 0.5,
        },
        width=900,
        height=max(500, 30 + len(display_df) * 25),
        margin={
            "l": 20,
            "r": 20,
            "t": 60,
            "b": 20,
        },
        autosize=False,
    )

    return fig


metrics = build_all_history_metrics((2,), (6,))

pearson_corr = metrics.select_dtypes(include="number").corr(method="pearson")

spearman_corr = metrics.select_dtypes(include="number").corr(method="spearman")

spearman_fig = plot_correlation_matrix(
    spearman_corr,
    "2d6 Metric Correlations — Spearman",
)
pearson_fig = plot_correlation_matrix(pearson_corr, "2d6 Metric Correlations - Pearson")

spearman_ranked = rank_correlations(spearman_corr)

pearson_ranked = rank_correlations(pearson_corr)

fig_path = "/Users/jamesekern/pythonProjects/gamblint/research/figures/game_analysis"

spearman_ranking_fig = plot_correlation_ranking(
    spearman_ranked, "Spearman Corelation Rankings"
)

pearson_ranking_fig = plot_correlation_ranking(
    pearson_ranked, "Pearson Corelation Rankings"
)

pearson_fig.write_image(f"{fig_path}/pearson_correlation_matrix.png", scale=2)
spearman_fig.write_image(f"{fig_path}/spearman_correlation_matrix.png", scale=2)
pearson_ranking_fig.write_image(f"{fig_path}/pearson_ranked_correlations.png", scale=2)
spearman_ranking_fig.write_image(
    f"{fig_path}/spearman_ranked_correlations.png", scale=2
)
