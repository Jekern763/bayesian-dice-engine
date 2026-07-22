# make a separate function to save every graph type. Build them as I go through graphs, then reuse
from pathlib import Path

import graph_config
import plotly.express as px


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
        font=dict(size=graph_config.FONT_SIZE),
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
        font=dict(size=18),
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
