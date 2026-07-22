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
