# make a separate function to save every graph type. Build them as I go through graphs, then reuse
from pathlib import Path

import graph_config
import plotly.express as px
import plotly.graph_objects as go


def save_line(
    df,
    x,
    y,
    title,
    x_label,
    y_label,
    output_path,
    color=None,
    markers=True,
):
    """
    Creates and saves a standardized line graph.
    """

    fig = px.line(
        df,
        x=x,
        y=y,
        color=color,
        markers=markers,
        title=title,
    )

    fig.update_layout(
        width=graph_config.WIDTH,
        height=graph_config.HEIGHT,
        template="simple_white",
        font={"size": graph_config.FONT_SIZE},
        title_font_size=24,
        xaxis_title=x_label,
        yaxis_title=y_label,
        legend_title_text="",
    )

    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    fig.write_image(output_path)


def save_bar(
    df,
    x,
    y,
    title,
    x_label,
    y_label,
    output_path,
    color=None,
):
    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        text_auto=".3f",
    )

    # Place labels outside the bars so zeros still show
    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
    )

    fig.update_layout(
        width=graph_config.WIDTH,
        height=graph_config.HEIGHT,
        template="simple_white",
        font={"size": 18},
        title_font_size=24,
        xaxis_title=x_label,
        yaxis_title=y_label,
        legend_title_text="",
    )

    fig.update_xaxes(type="category")
    fig.update_yaxes(showgrid=True)

    # Draw the x-axis (y = 0) explicitly
    fig.add_hline(
        y=0,
        line_width=2,
        line_color="black",
    )

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    fig.write_image(output_path)


def save_scatter(
    df,
    x,
    y,
    label,
    title,
    x_label,
    y_label,
    output_path,
    color=None,
    x_axis_type="-",
    y_axis_type="-",
    textposition="top right",
):
    plot_df = df.copy()

    plot_df[label] = (
        plot_df[label]
        .str.replace("_agent", "", regex=False)
        .str.replace("_", " ")
        .str.title()
    )
    fig = px.scatter(
        plot_df,
        x=x,
        y=y,
        text=label,
        color=color,
        title=title,
    )

    fig.update_traces(
        mode="markers+text",
        textposition=textposition,
        marker={"size": 10},
    )

    fig.update_layout(
        width=graph_config.WIDTH,
        height=graph_config.HEIGHT,
        template="simple_white",
        font={"size": graph_config.FONT_SIZE},
        title_font_size=24,
        xaxis_title=x_label,
        yaxis_title=y_label,
        legend_title_text="",
    )

    fig.update_xaxes(showgrid=True, type=x_axis_type, autorange=True)
    fig.update_yaxes(showgrid=True, type=y_axis_type, autorange=True)
    fig.update_traces(cliponaxis=False)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    fig.write_image(output_path)


# a function to graph all algorithms on one graph


def save_multi_line(
    dfs: dict,
    x,
    y,
    title,
    x_label,
    y_label,
    output_path,
):
    fig = go.Figure()

    for name, df in dfs.items():
        fig.add_trace(
            go.Scatter(
                x=df[x],
                y=df[y],
                mode="lines+markers",
                name=(name.replace("_agent", "").replace("_", " ").title()),
            )
        )

    fig.update_layout(
        width=graph_config.WIDTH,
        height=graph_config.HEIGHT,
        template="simple_white",
        font={"size": graph_config.FONT_SIZE},
        title=title,
        title_font_size=24,
        xaxis_title=x_label,
        yaxis_title=y_label,
        legend_title_text="Algorithm",
    )

    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True, rangemode="tozero")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    fig.write_image(output_path)
