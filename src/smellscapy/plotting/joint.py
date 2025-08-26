import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from smellscapy.calculations import calculate_pleasantness, calculate_presence
from matplotlib.ticker import MultipleLocator
from matplotlib.gridspec import GridSpec


def plot_joint(df, **kwargs):
    """
    Joint plot con:
    - scatter + contour HDR 50%
    - assi ortogonali e diagonali
    - etichette dei quadranti
    - griglia con stili diversi per tick maggiori/minori
    - marginali 1D (KDE) in alto e a destra
    - supporto opzionale a gruppi (group_col)
    """

    # Dictionary default values
    params = {

        "xlim": (-1, 1),
        "ylim": (-1, 1),
        "figsize": (8, 8),

        # Punti e contour
        "point_alpha": 0.8,
        "point_color": "grey",
        "point_size": 30,
        "contour_alpha": 0.6,
        "contour_color": "black",
        "contour_width": 1,

        # Etichette assi
        "xlabel": "Pleasantness",
        "ylabel": "Presence",

        # Assi centrali
        "axis_line_color": "grey",
        "axis_line_style": "-",
        "axis_line_width": 0.5,

        # Diagonali
        "diag_color": "grey",
        "diag_style": "--",
        "diag_width": 0.5,

        # Etichette quadranti
        "labels": {
            "overpowering": {"pos": (-0.5,  0.5), "text": "Overpowering"},
            "detached":     {"pos": (-0.5, -0.5), "text": "Detached"},
            "engaging":     {"pos": ( 0.5,  0.5), "text": "Engaging"},
            "light":        {"pos": ( 0.5, -0.5), "text": "Light"},
        },
        "labels_style": {"fontsize": 10, "fontstyle": "italic", "alpha": 0.7},

        "fontsize": 10,

        # Salvataggio
        "savefig": True,
        "filename": "joint_plot.png",
        "dpi": 300,

        # Raggruppamento
        "group_col": None,

        # >>> Griglia/ticks (NUOVO) <<<
        "xmajor_step": 0.25, "xminor_step": 0.05,
        "ymajor_step": 0.25, "yminor_step": 0.05,
        "grid_major": {"linestyle": "--", "linewidth": 0.9, "alpha": 0.7},
        "grid_minor": {"linestyle": ":",  "linewidth": 0.5, "alpha": 0.35},
        "minor_tick_length": 0,  # 0 = nasconde le tacche minori

        # >>> Marginali (NUOVO) <<<
        "marginal_color": "black",
        "marginal_alpha": 0.85,
        "marginal_linewidth": 1.2,
        "grid_size": 200
    }

    # Update only the parameters provided by the user
    for key, value in kwargs.items():
        if key in params and isinstance(params[key], dict) and isinstance(value, dict):
            params[key].update(value)  # merge dict (es. labels)
        else:
            params[key] = value
    # Dati base
    X = df["pleasantness_score"].values
    Y = df["presence_score"].values

    fig = plt.figure(figsize=params["figsize"])

    gs = GridSpec(4, 4, figure=fig, wspace=0.05, hspace=0.05)
    ax_main = fig.add_subplot(gs[1:4, 0:3])
    ax_top  = fig.add_subplot(gs[0,    0:3], sharex=ax_main)
    ax_right= fig.add_subplot(gs[1:4, 3],   sharey=ax_main)

    # Helper: plot gruppo su ax_main
    def plot_group(x, y, label=None, color=None):
        xy = np.vstack([x, y])
        kde = gaussian_kde(xy)
        z = kde(xy)

        # Soglia 50% HDR
        z_sorted = np.sort(z)
        cdf = np.cumsum(z_sorted) / np.sum(z_sorted)
        z_50 = z_sorted[np.searchsorted(cdf, 0.5)]

        # Griglia per contour
        xi, yi = np.mgrid[
            params["xlim"][0]:params["xlim"][1]:100j,
            params["ylim"][0]:params["ylim"][1]:100j
        ]
        zi = kde(np.vstack([xi.ravel(), yi.ravel()])).reshape(xi.shape)

        # Contour/fill 50%
        ax_main.contourf(
            xi, yi, zi,
            levels=[z_50, zi.max()],
            colors=[color if color else params["point_color"]],
            alpha=params["contour_alpha"]
        )
        ax_main.contour(
            xi, yi, zi,
            levels=[z_50],
            colors=color if color else params["contour_color"],
            linewidths=params["contour_width"]
        )

        # Scatter
        ax_main.scatter(x, y,
                        s=params["point_size"],
                        color=color if color else params["point_color"],
                        alpha=params["point_alpha"],
                        label=label)

    # Plot principale (eventuale grouping)
    if params["group_col"] is not None and params["group_col"] in df.columns:
        import itertools
        color_cycle = itertools.cycle(plt.cm.tab20.colors)
        for name, g in df.groupby(params["group_col"]):
            c = next(color_cycle)
            plot_group(g["pleasantness_score"].values,
                       g["presence_score"].values,
                       label=str(name), color=c)
        ax_main.legend(title=params["group_col"])
    else:
        plot_group(X, Y)

    # Limiti/etichette
    ax_main.set_xlim(params["xlim"])
    ax_main.set_ylim(params["ylim"])
    ax_main.set_xlabel(params["xlabel"])
    ax_main.set_ylabel(params["ylabel"])

    # Ticks e griglia (stili diversi)
    ax_main.xaxis.set_major_locator(MultipleLocator(params["xmajor_step"]))
    ax_main.xaxis.set_minor_locator(MultipleLocator(params["xminor_step"]))
    ax_main.yaxis.set_major_locator(MultipleLocator(params["ymajor_step"]))
    ax_main.yaxis.set_minor_locator(MultipleLocator(params["yminor_step"]))
    ax_main.set_axisbelow(True)
    ax_main.grid(True, which="major", **params["grid_major"])
    ax_main.grid(True, which="minor", **params["grid_minor"])
    ax_main.tick_params(which="minor", length=params["minor_tick_length"])

    # Assi centrali
    ax_main.axhline(0, color=params["axis_line_color"],
                    linestyle=params["axis_line_style"],
                    linewidth=params["axis_line_width"])
    ax_main.axvline(0, color=params["axis_line_color"],
                    linestyle=params["axis_line_style"],
                    linewidth=params["axis_line_width"])

    # Diagonali
    x_vals = np.linspace(params["xlim"][0], params["xlim"][1], 200)
    ax_main.plot(x_vals,  x_vals, linestyle=params["diag_style"],
                 color=params["diag_color"], linewidth=params["diag_width"])
    ax_main.plot(x_vals, -x_vals, linestyle=params["diag_style"],
                 color=params["diag_color"], linewidth=params["diag_width"])

    # Etichette dei quadranti
    for lbl in params["labels"].values():
        ax_main.text(lbl["pos"][0], lbl["pos"][1], lbl["text"],
                ha="center", va="center", **params["labels_style"])

    # --- Marginali 1D (KDE) ---
    if params["group_col"] is not None and params["group_col"] in df.columns:
        import itertools
        color_cycle = itertools.cycle(plt.cm.tab20.colors)
        for name, g in df.groupby(params["group_col"]):
            c = next(color_cycle)
            kde_x = gaussian_kde(g["pleasantness_score"].values)
            kde_y = gaussian_kde(g["presence_score"].values)
            xx = np.linspace(params["xlim"][0], params["xlim"][1], params["grid_size"])
            yy = np.linspace(params["ylim"][0], params["ylim"][1], params["grid_size"])
            ax_top.plot(xx, kde_x(xx), color=c,
                        alpha=params["marginal_alpha"],
                        linewidth=params["marginal_linewidth"])
            ax_right.plot(kde_y(yy), yy, color=c,
                          alpha=params["marginal_alpha"],
                          linewidth=params["marginal_linewidth"])
    else:
        kde_x = gaussian_kde(X)
        kde_y = gaussian_kde(Y)
        xx = np.linspace(params["xlim"][0], params["xlim"][1], params["grid_size"])
        yy = np.linspace(params["ylim"][0], params["ylim"][1], params["grid_size"])
        ax_top.plot(xx, kde_x(xx), color=params["marginal_color"],
                    alpha=params["marginal_alpha"],
                    linewidth=params["marginal_linewidth"])
        ax_right.plot(kde_y(yy), yy, color=params["marginal_color"],
                      alpha=params["marginal_alpha"],
                      linewidth=params["marginal_linewidth"])

    # Mostra solo le curve sui marginali
    ax_top.axis("off")
    ax_right.axis("off")

    # Layout e salvataggio
    plt.tight_layout()
    if params["savefig"]:
        fig.savefig(params["filename"], dpi=params["dpi"], bbox_inches="tight")
    plt.show()