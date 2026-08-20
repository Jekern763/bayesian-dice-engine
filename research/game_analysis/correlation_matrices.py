import numpy as np
import pandas as pd
import plotly.graph_objects as go
from analysis_by_history import build_all_history_metrics
from sklearn.metrics import normalized_mutual_info_score


def plot_correlation_matrix(
    corr: pd.DataFrame,
    title: str = "Correlation Matrix",
    scale: str = "signed",
):
    """
    Plot a correlation/dependence matrix.

    scale:
        "signed"   -> -1 to 1, for Pearson/Spearman
        "unsigned" -> 0 to 1, for normalized mutual information
    """

    if scale == "unsigned":
        zmin = 0
        zmax = 1
        colorbar_title = "Dependence"
        value_label = "Normalized Mutual Information"
    else:
        zmin = -1
        zmax = 1
        colorbar_title = "Correlation"
        value_label = "Correlation"

    fig = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.index,
            zmin=zmin,
            zmax=zmax,
            text=corr.round(2).values,
            texttemplate="%{text}",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "<b>%{x}</b><br>"
                f"{value_label}: %{{z:.4f}}"
                "<extra></extra>"
            ),
            colorbar={
                "title": colorbar_title,
            },
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


def discretize_numeric_metrics(
    df: pd.DataFrame,
    n_bins: int = 50,
) -> pd.DataFrame:
    """
    Convert numeric metrics into quantile-based discrete bins.

    Quantile bins attempt to put approximately the same number
    of observations into each bin.

    This makes the NMI calculation much more robust to metrics
    with very different scales.
    """

    numeric_df = df.select_dtypes(include="number")

    binned = pd.DataFrame(
        index=numeric_df.index,
        columns=numeric_df.columns,
        dtype="int64",
    )

    for column in numeric_df.columns:
        series = numeric_df[column]

        # Remove infinities before binning.
        series = series.replace(
            [np.inf, -np.inf],
            np.nan,
        )

        try:
            binned[column] = pd.qcut(
                series,
                q=n_bins,
                labels=False,
                duplicates="drop",
            )
        except ValueError:
            # A metric with too few unique values cannot be
            # split into the requested number of bins.
            binned[column] = pd.factorize(
                series,
                sort=True,
            )[0]

    return binned


def calculate_nmi_matrix(
    df: pd.DataFrame,
    n_bins: int = 20,
    sample_size: int | None = 50_000,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Calculate a normalized mutual-information matrix.

    Values range from 0 to 1:

        0 = independent / little detectable dependence
        1 = identical information

    The metrics are first discretized into quantile bins.

    Parameters
    ----------
    df:
        DataFrame containing numeric metrics.

    n_bins:
        Number of quantile bins used for each metric.

    sample_size:
        Maximum number of rows used. Set to None to use all rows.

    random_state:
        Random seed used when sampling.
    """

    numeric_df = df.select_dtypes(include="number").copy()

    # Remove infinities.
    numeric_df = numeric_df.replace(
        [np.inf, -np.inf],
        np.nan,
    )

    # Sampling is useful for very large datasets.
    # NMI doesn't need millions of observations to identify
    # broad nonlinear relationships.
    if sample_size is not None and len(numeric_df) > sample_size:
        numeric_df = numeric_df.sample(
            n=sample_size,
            random_state=random_state,
        )

    # Discretize all metrics once.
    binned = discretize_numeric_metrics(
        numeric_df,
        n_bins=n_bins,
    )

    columns = binned.columns

    result = pd.DataFrame(
        np.eye(len(columns)),
        index=columns,
        columns=columns,
        dtype=float,
    )

    # Calculate pairwise NMI.
    for i, col1 in enumerate(columns):
        for j in range(i + 1, len(columns)):
            col2 = columns[j]

            pair = binned[[col1, col2]].dropna()

            if len(pair) < 2:
                value = np.nan
            else:
                value = normalized_mutual_info_score(
                    pair[col1].to_numpy(),
                    pair[col2].to_numpy(),
                    average_method="arithmetic",
                )

            result.loc[col1, col2] = value
            result.loc[col2, col1] = value

    return result


def calculate_correlation_matrix(
    df: pd.DataFrame,
    method: str = "pearson",
    n_bins: int = 50,
    mi_sample_size: int | None = 50_000,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Calculate relationships between all numeric metrics.

    Methods:

        pearson
            Linear correlation.
            Range: -1 to 1.

        spearman
            Monotonic correlation.
            Range: -1 to 1.

        nmi
            Normalized mutual information.
            Detects arbitrary dependence, including
            non-monotonic relationships.
            Range: 0 to 1.
    """

    numeric_df = df.select_dtypes(include="number")

    if method in ("pearson", "spearman"):
        return numeric_df.corr(method=method)

    if method == "nmi":
        return calculate_nmi_matrix(
            numeric_df,
            n_bins=n_bins,
            sample_size=mi_sample_size,
            random_state=random_state,
        )

    raise ValueError(
        f"Unknown correlation method: {method}. Use 'pearson', 'spearman', or 'nmi'."
    )


def rank_correlations(
    corr: pd.DataFrame,
    min_strength: float = 0.60,
    unsigned: bool = False,
) -> pd.DataFrame:
    rows, cols = np.triu_indices_from(corr, k=1)

    ranked = pd.DataFrame(
        {
            "metric_1": corr.index[rows],
            "metric_2": corr.columns[cols],
            "correlation": corr.values[rows, cols],
        }
    )

    if unsigned:
        ranked["strength"] = ranked["correlation"]
    else:
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


# ============================================================================
# Build metrics
# ============================================================================

metrics = build_all_history_metrics((2,), (6,))


# ============================================================================
# Calculate correlations
# ============================================================================

pearson_corr = calculate_correlation_matrix(
    metrics,
    method="pearson",
)

spearman_corr = calculate_correlation_matrix(
    metrics,
    method="spearman",
)

nmi_corr = calculate_correlation_matrix(
    metrics,
    method="nmi",
    n_bins=50,
    mi_sample_size=50_000,
)


# ============================================================================
# Create correlation matrix figures
# ============================================================================

pearson_fig = plot_correlation_matrix(
    pearson_corr,
    "2d6 Metric Correlations — Pearson",
)

spearman_fig = plot_correlation_matrix(
    spearman_corr,
    "2d6 Metric Correlations — Spearman",
)

nmi_fig = plot_correlation_matrix(
    nmi_corr,
    "2d6 Metric Dependencies — Normalized Mutual Information",
    scale="unsigned",
)


# ============================================================================
# Rank correlations
# ============================================================================

pearson_ranked = rank_correlations(
    pearson_corr,
)

spearman_ranked = rank_correlations(
    spearman_corr,
)

nmi_ranked = rank_correlations(
    nmi_corr,
    unsigned=True,
)


# ============================================================================
# Create ranking figures
# ============================================================================

pearson_ranking_fig = plot_correlation_ranking(
    pearson_ranked,
    "Pearson Correlation Rankings",
)

spearman_ranking_fig = plot_correlation_ranking(
    spearman_ranked,
    "Spearman Correlation Rankings",
)

nmi_ranking_fig = plot_correlation_ranking(
    nmi_ranked,
    "Normalized Mutual Information Rankings",
)


# ============================================================================
# Save figures
# ============================================================================

fig_path = "/Users/jamesekern/pythonProjects/gamblint/research/figures/game_analysis"

pearson_fig.write_image(
    f"{fig_path}/pearson_correlation_matrix.png",
    scale=2,
)

spearman_fig.write_image(
    f"{fig_path}/spearman_correlation_matrix.png",
    scale=2,
)

nmi_fig.write_image(
    f"{fig_path}/nmi_matrix.png",
    scale=2,
)

pearson_ranking_fig.write_image(
    f"{fig_path}/pearson_ranked_correlations.png",
    scale=2,
)

spearman_ranking_fig.write_image(
    f"{fig_path}/spearman_ranked_correlations.png",
    scale=2,
)

nmi_ranking_fig.write_image(
    f"{fig_path}/nmi_ranked_correlations.png",
    scale=2,
)
