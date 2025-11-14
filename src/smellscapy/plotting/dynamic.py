import numpy as np
import pandas as pd
from typing import List, Dict
import plotly.graph_objects as go
import smellscapy.plotting.utils as ut


def plot_dynamic(df: pd.DataFrame, time_col: str, **kwargs) -> go.Figure:
    """
    Creates an animated 50% Highest Density Region (HDR) plot in the Pleasantness-Presence space,
    based on time-varying survey data.

    This function computes a kernel density estimation (KDE) for each time step defined in
    `time_col`, builds the corresponding 50% HDR contour, and assembles all frames into an
    interactive Plotly animation. If a grouping column is provided, separate HDR contours are
    generated per category with a stable colour map across frames.

    Plot appearance, animation behaviour, KDE resolution, colours, axis limits, annotations,
    and output options can be customised through `**kwargs`.

    Parameters
    ----------
    df : pd.DataFrame
        A DataFrame containing the input data. It must include at least the columns  
        `'pleasantness_score'`, `'presence_score'`, and the time variable specified in `time_col`.

    time_col : str
        Name of the column defining the temporal sequence for animation frames.

    **kwargs : dict, optional**
        Additional keyword arguments to override default plotting parameters, including:
        - `group_by_col` : str, column used to generate category-specific HDR contours.  
        - `xlim`, `ylim` : tuple of float, axis limits for Pleasantness and Presence.  
        - `eval_n` : int, resolution of the KDE evaluation grid.  
        - `palette` : list or dict, custom colour palette for categories.  
        - `frame_order` : list, custom ordering of animation frames.  
        - `labels` : dict, annotation labels to display in the plot.  
        - `write_html` : str, path to export the animation as an HTML file.  
        - `auto_open` : bool, whether to open the exported HTML automatically.  
        - `show` : bool, display the animated figure in the notebook or interface.

    Returns
    -------
    fig : plotly.graph_objects.Figure  
        A fully configured Plotly figure containing HDR contours, animation frames,
        slider controls, and play/pause buttons.

    Examples
    --------
        >>> from smellscapy.plotting import plot_dynamic
        >>> fig = plot_dynamic(df, time_col="How long have you been in your office without leaving?", group_by_col="Smell source")
        >>> fig.show()

    """

    # ------------------------------------------------------------------
    # Parameters
    # ------------------------------------------------------------------
    params = ut.get_default_dynamic_plot_params()
    params = ut.update_params(params, **kwargs)

    x_col = "pleasantness_score"
    y_col = "presence_score"
    group_col = params.get("group_by_col", None)

    xlim = tuple(params["xlim"])
    ylim = tuple(params["ylim"])
    eval_n = int(params["eval_n"])

    frame_order = params.get("frame_order", None)

    # ------------------------------------------------------------------
    # Global categories and global colour map
    # ------------------------------------------------------------------
    if group_col and group_col in df.columns:
        all_cats = df[group_col].dropna()
        global_categories: List[str] = sorted(all_cats.unique(), key=str)
    else:
        global_categories = []

    def _build_global_color_map(order: List[str]) -> Dict[str, str]:
        palette = params.get("palette", None)

        # palette as dict {cat: colour}
        if isinstance(palette, dict):
            return {cat: palette.get(cat, "#0033FF") for cat in order}

        # palette as list or default
        default = [
            "#636EFA", "#EF553B", "#336759", "#00FF6E", "#F78F40",
            "#00D9FF", "#C67F93", "#B6E880", "#EE00EE", "#6C634D"
        ]
        if isinstance(palette, list) and len(palette) >= len(order):
            seq = palette
        else:
            seq = default

        return {cat: seq[i % len(seq)] for i, cat in enumerate(order)}

    if global_categories:
        global_color_map = _build_global_color_map(global_categories)
    else:
        global_color_map = {}

    # ------------------------------------------------------------------
    # KDE grid
    # ------------------------------------------------------------------
    xi = np.linspace(xlim[0], xlim[1], eval_n)
    yi = np.linspace(ylim[0], ylim[1], eval_n)
    XX, YY = np.meshgrid(xi, yi, indexing="xy")

    # ------------------------------------------------------------------
    # Helper: KDE / HDR
    # ------------------------------------------------------------------
    def _compute_hdr_field(x: np.ndarray,
                           y: np.ndarray,
                           hdr_prob: float = 0.5) -> tuple[np.ndarray, float]:
        """
        Return (Z_norm, thr) where Z_norm in [0,1],
        and thr is the HDR threshold in the same [0,1] scale.
        """
        if x.size == 0 or y.size == 0:
            return np.full_like(XX, np.nan, dtype=float), np.nan

        Z = ut.kde_on_grid(x, y, XX, YY)

        if Z is None:
            return np.full_like(XX, np.nan, dtype=float), np.nan
        if isinstance(Z, tuple):
            Z = Z[0]

        Z = np.asarray(Z, dtype=float)

        finite_mask = np.isfinite(Z)
        if not finite_mask.any():
            return np.full_like(XX, np.nan, dtype=float), np.nan

        lvl = ut._hdr_level(Z, hdr_prob)
        if not np.isfinite(lvl):
            return np.full_like(XX, np.nan, dtype=float), np.nan

        z_finite = Z[finite_mask]
        z_min = float(z_finite.min())
        z_max = float(z_finite.max())

        if not np.isfinite(z_min) or not np.isfinite(z_max) or z_max == z_min:
            return np.full_like(XX, np.nan, dtype=float), np.nan

        denom = z_max - z_min
        Z_norm = (Z - z_min) / denom
        thr = (lvl - z_min) / denom

        return Z_norm, thr

    # ------------------------------------------------------------------
    # Trace for ONE category in ONE frame (grouped case)
    # ------------------------------------------------------------------
    def _trace_for_category(subdf: pd.DataFrame,
                            cat: str) -> go.Contour:
        """
        Always returns a trace for category 'cat'.
        If there are no data or HDR is not defined, the trace is transparent.
        """
        if group_col is None or group_col not in subdf.columns:
            return go.Contour(
                x=xi,
                y=yi,
                z=np.full_like(XX, np.nan, dtype=float),
                showscale=False,
                colorscale=[
                    [0.0, "rgba(0,0,0,0)"],
                    [1.0, "rgba(0,0,0,0)"],
                ],
                showlegend=False,
                opacity=0.0,
                name=str(cat),
                legendgroup=str(cat),
            )

        mask = (subdf[group_col] == cat).values
        x = subdf.loc[mask, x_col].to_numpy()
        y = subdf.loc[mask, y_col].to_numpy()

        Z_norm, thr = _compute_hdr_field(x, y, hdr_prob=0.5)

        # No HDR → transparent trace, keeps structure for animation
        if not np.isfinite(thr):
            return go.Contour(
                x=xi,
                y=yi,
                z=np.full_like(XX, np.nan, dtype=float),
                showscale=False,
                colorscale=[
                    [0.0, "rgba(0,0,0,0)"],
                    [1.0, "rgba(0,0,0,0)"],
                ],
                showlegend=False,
                opacity=0.0,
                name=str(cat),
                legendgroup=str(cat),
            )

        color = global_color_map.get(cat, "#0033FF")

        return go.Contour(
            x=xi,
            y=yi,
            z=Z_norm,
            showscale=False,
            colorscale=[
                [0.0, "rgba(0,0,0,0)"],
                [max(thr - 1e-6, 0.0), "rgba(0,0,0,0)"],
                [thr, color],
                [1.0, color],
            ],
            showlegend=False,   # legend is manged with "fake" scatters
            opacity=0.35,
            contours=dict(
                start=thr,
                end=1.0,
                size=1.0 - thr,
                coloring="fill",
                showlines=False,
            ),
            line=dict(width=0),
            name=str(cat),
            legendgroup=str(cat),
        )

    # ------------------------------------------------------------------
    # Ungrouped case
    # ------------------------------------------------------------------
    def _make_traces_ungrouped(subdf: pd.DataFrame, show_legend: bool = True):
        traces: List[go.BaseTraceType] = []
        x = subdf[x_col].to_numpy()
        y = subdf[y_col].to_numpy()
        Z_norm, thr = _compute_hdr_field(x, y, hdr_prob=0.5)
        if not np.isfinite(thr):
            return []
        traces.append(
            go.Contour(
                x=xi,
                y=yi,
                z=Z_norm,
                showscale=False,
                colorscale=[
                    [0.0, "rgba(0,0,0,0)"],
                    [max(thr - 1e-6, 0.0), "rgba(0,0,0,0)"],
                    [thr, "rgba(255,192,203,1)"],
                    [1.0, "rgba(255,192,203,1)"],
                ],
                showlegend=show_legend,
                opacity=0.4,
                contours=dict(
                    start=thr,
                    end=1.0,
                    size=1.0 - thr,
                    coloring="fill",
                    showlines=False,
                ),
                line=dict(width=0),
                name="HDR 50%",
            )
        )
        return traces

    # ------------------------------------------------------------------
    # Animation: frames and initial figure
    # ------------------------------------------------------------------
    values = df[time_col]
    ordered_values = ut.order_values_for_frames(df[time_col], order_override=frame_order)

    frames: List[go.Frame] = []

    if group_col and group_col in df.columns and global_categories:
        # ---- grouped case: same traces structure in every frame
        for val in ordered_values:
            sub = df[values == val]
            frame_traces = []
            for cat in global_categories:
                frame_traces.append(_trace_for_category(sub, cat))
            frames.append(go.Frame(name=str(val), data=frame_traces))

        # initial data (first frame)
        initial_sub = df[values == ordered_values[0]]
        initial_traces = []
        for cat in global_categories:
            initial_traces.append(_trace_for_category(initial_sub, cat))

        fig = go.Figure(data=initial_traces, frames=frames)

    else:
        # ---- ungrouped case
        for val in ordered_values:
            sub = df[values == val]
            traces = _make_traces_ungrouped(sub, show_legend=False)
            frames.append(go.Frame(name=str(val), data=traces))

        initial_sub = df[values == ordered_values[0]]
        fig = go.Figure(
            data=_make_traces_ungrouped(initial_sub, show_legend=True),
            frames=frames,
        )

    # ------------------------------------------------------------------
    # Stable legend: one fake Scatter per category (grouped only)
    # ------------------------------------------------------------------
    if group_col and group_col in df.columns and global_categories:
        for cat in global_categories:
            fig.add_trace(
                go.Scatter(
                    x=[None],
                    y=[None],
                    mode="markers",
                    marker=dict(
                        size=10,
                        color=global_color_map.get(cat, "#0033FF"),
                    ),
                    name=str(cat),
                    legendgroup=str(cat),
                    showlegend=True,
                    hoverinfo="skip",
                )
            )

    # ------------------------------------------------------------------
    # Slider steps
    # ------------------------------------------------------------------
    steps = []
    for v in ordered_values:
        steps.append(
            {
                "method": "animate",
                "label": str(v),
                "args": [
                    [str(v)],
                    {
                        "mode": "immediate",
                        "transition": {"duration": 0},
                        "frame": {"duration": 0, "redraw": True},
                    },
                ],
            }
        )

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------
    major_step = 0.25
    minor_step = 0.05

    xmin, xmax = xlim
    ymin, ymax = ylim

    xticks = np.arange(xmin, xmax + 1e-4, minor_step)
    yticks = np.arange(ymin, ymax + 1e-4, minor_step)

    def _tick_labels(vals: np.ndarray) -> List[str]:
        labels = []
        for v in vals:
            if abs(v % major_step) < 1e-8:
                labels.append(f"{v:.2f}")
            else:
                labels.append("")
        return labels

    xticktext = _tick_labels(xticks)
    yticktext = _tick_labels(yticks)

    fig.update_layout(
        xaxis=dict(
            range=[xmin, xmax],
            constrain="domain",
            tickvals=xticks,
            ticktext=xticktext,
            tickfont=dict(size=12),
            tickcolor="black",
            tickwidth=2,
            ticklen=8,
            minor=dict(
                tick0=0,
                dtick=minor_step,
                ticklen=0,
                tickwidth=1,
                tickcolor="rgba(0,0,0,0.4)",
            ),
        ),
        yaxis=dict(
            range=[ymin, ymax],
            scaleanchor="x",
            scaleratio=1,
            tickvals=yticks,
            ticktext=yticktext,
            tickfont=dict(size=12),
            tickcolor="black",
            tickwidth=2,
            ticklen=8,
            minor=dict(
                tick0=0,
                dtick=minor_step,
                ticklen=0,
                tickwidth=1,
                tickcolor="rgba(0,0,0,0.4)"
            ),
        ),
        xaxis_title="Pleasantness",
        yaxis_title="Presence",
        paper_bgcolor="white",
        plot_bgcolor="white",
        title="Simple Density (HDR 50%)",
        updatemenus=[
            {
                "type": "buttons",
                "showactive": False,
                "buttons": [
                    {
                        "label": "▶ Play",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "fromcurrent": True,
                                "frame": {
                                    "duration": 500,
                                    "redraw": True,
                                },
                                "transition": {"duration": 200},
                            },
                        ],
                    },
                    {
                        "label": "⏸ Pause",
                        "method": "animate",
                        "args": [
                            [None],
                            {
                                "mode": "immediate",
                                "frame": {
                                    "duration": 0,
                                    "redraw": False,
                                },
                            },
                        ],
                    },
                ],
                "x": 0.02,
                "y": 0.5,
                "xanchor": "left",
                "yanchor": "top",
            }
        ],
        sliders=[
            {
                "active": 0,
                "x": 0.02,
                "y": -0.06,
                "xanchor": "left",
                "yanchor": "top",
                "len": 0.96,
                "pad": {"t": 5, "b": 0},
                "steps": steps,
            }
        ],
    )

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------
    for yy in [0]:
        fig.add_hline(
            y=yy,
            line_color="grey",
            line_width=0.5,
            line_dash="solid",
        )

    for xx in [0]:
        fig.add_vline(
            x=xx,
            line_color="grey",
            line_width=0.5,
            line_dash="solid",
        )

    for yy in [1, -1]:
        fig.add_hline(
            y=yy,
            line_color="black",
            line_width=1,
            line_dash="solid",
        )

    for xx in [1, -1]:
        fig.add_vline(
            x=xx,
            line_color="black",
            line_width=1,
            line_dash="solid",
        )

    for yy in [-0.75, -0.5, -0.25, 0.75, 0.5, 0.25]:
        fig.add_hline(
            y=yy,
            line_color="grey",
            line_width=0.1,
            line_dash="solid",
        )

    for xx in [-0.75, -0.5, -0.25, 0.75, 0.5, 0.25]:
        fig.add_vline(
            x=xx,
            line_color="grey",
            line_width=0.1,
            line_dash="solid",
        )

    x_vals = np.linspace(xmin, xmax, 200)

    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=x_vals,
            mode="lines",
            line=dict(
                color="grey",
                width=0.5,
                dash="dot",
            ),
            showlegend=False,
            hoverinfo="skip",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=-x_vals,
            mode="lines",
            line=dict(
                color="grey",
                width=0.5,
                dash="dot",
            ),
            showlegend=False,
            hoverinfo="skip",
        )
    )

    for lbl in params.get("labels", {}).values():
        fig.add_annotation(
            x=lbl["pos"][0],
            y=lbl["pos"][1],
            text=lbl["text"],
            showarrow=False,
            xanchor="center",
            yanchor="middle",
            font=dict(
                family="Arial",
                size=10,
                color="rgba(0,0,0,0.7)",
            ),
        )

    # ------------------------------------------------------------------
    # Save/show
    # ------------------------------------------------------------------
    if params.get("write_html"):
        fig.write_html(params["write_html"], auto_open=params.get("auto_open", False))

    if params.get("show"):
        try:
            import plotly.io as pio  # noqa: F401
        except Exception:
            pass
        fig.show()

    return fig
