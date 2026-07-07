from pathlib import Path

import numpy as np
import plotly.graph_objects as go

# ==========================================================
# Payout Function
# ==========================================================


def payout(g, R):
    return (2 - np.abs(R - g)) * np.abs(7 - g)


# ==========================================================
# Continuous grid
# ==========================================================

resolution = 1000

R_vals = np.linspace(2, 12, resolution)
g_vals = np.linspace(2, 12, resolution)

RR, GG = np.meshgrid(R_vals, g_vals)

Z = payout(GG, RR)

# ==========================================================
# Heatmap
# ==========================================================

heatmap = go.Heatmap(
    x=R_vals,
    y=g_vals,
    z=Z,
    colorscale="Plasma",
    colorbar=dict(title="Payout"),
    visible=True,
)

# ==========================================================
# Contour
# ==========================================================

contour = go.Contour(
    x=R_vals,
    y=g_vals,
    z=Z,
    contours=dict(showlabels=True),
    colorbar=dict(title="Payout"),
    visible=False,
)


fig = go.Figure(data=[heatmap, contour])

# ==========================================================
# Dropdowns
# ==========================================================

plot_buttons = [
    dict(
        label="Heatmap",
        method="update",
        args=[{"visible": [True, False, heatmap.visible, contour.visible]}],
    ),
    dict(
        label="Contour",
        method="update",
        args=[{"visible": [False, True, heatmap.visible, contour.visible]}],
    ),
]


fig.update_layout(
    title="Payout Function with Optimal Guess",
    xaxis_title="Roll (R)",
    yaxis_title="Guess (g)",
    width=900,
    height=700,
    updatemenus=[dict(buttons=plot_buttons, direction="down", x=0.02, y=1.12)],
)

script_dir = Path(__file__).resolve().parent

output_path = script_dir.parent / "figures" / "payout.html"
fig.write_html(output_path)
