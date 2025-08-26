import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib.gridspec import GridSpec
from smellscapy.calculations import calculate_pleasantness, calculate_presence
from matplotlib.ticker import MultipleLocator

def plot_simple_density(df, **kwargs):
    """
    Density plot 2D (KDE) con:
    - contorno/fill al 50% HDR
    - assi ortogonali e diagonali
    - etichette dei quadranti
    - griglia con stili diversi per tick maggiori e minori
    - marginali 1D in alto e a destra
    - supporto opzionale a gruppi (group_col)
    """

    # Parametri di default
    params = {
        "xlim": (-1, 1),
        "ylim": (-1, 1),
        "figsize": (8, 8),
        "xlabel": "Pleasantness",
        "ylabel": "Presence",

        # Stile KDE/contorni
        "point_alpha": 0.6,
        "contour_color": "black",
        "contour_width": 1,
        "fill_color": "grey",

        # Assi centrali
        "axis_line_color": "grey",
        "axis_line_style": "-",
        "axis_line_width": 0.5,


        # Diagonali
        "diag_color": "grey",
        "diag_style": "--",
        "diag_width": 0.5,

        "labels": {
            "overpowering": {"pos": (-0.5, 0.5),"text": "Overpowering"},
            "detached": {"pos": (-0.5, -0.5),"text": "Detached"},
            "engaging": {"pos": (0.5, 0.5),"text": "Engaging"},
            "light": {"pos": (0.5, -0.5), "text": "Light"},
        },
        "labels_style": {"fontsize": 10, "fontstyle": "italic", "alpha": 0.7},

        "fontsize": 10,

        # Salvataggio
        "savefig": True,
        "filename": "simple_density_plot.png",
        "dpi": 300,

        # Raggruppamento opzionale
        "group_col": None,

        # Marginali
        "marginal_color": "black",
        "marginal_alpha": 0.8,
        "marginal_linewidth": 1.2,
        "grid_size": 200,

        # >>> Griglia/ticks (NUOVO) <<<
        "xmajor_step": 0.25, "xminor_step": 0.05,
        "ymajor_step": 0.25, "yminor_step": 0.05,
        "grid_major": {"linestyle": "--", "linewidth": 0.8, "alpha": 0.7},
        "grid_minor": {"linestyle": ":",  "linewidth": 0.5, "alpha": 0.35},
        "minor_tick_length": 0  # 0 = nasconde le tacchette minori
    }

    # Update con kwargs (merge per i dict)
    for key, value in kwargs.items():
        if key in params and isinstance(params[key], dict) and isinstance(value, dict):
            params[key].update(value)
        else:
            params[key] = value

    # Dati
    x = df["pleasantness_score"].values
    y = df["presence_score"].values

    # Griglia figure (main + marginali)
    fig = plt.figure(figsize=params["figsize"])
    gs = GridSpec(4, 4, figure=fig, wspace=0.05, hspace=0.05)
    ax_main = fig.add_subplot(gs[1:4, 0:3])
    ax_x = fig.add_subplot(gs[0, 0:3], sharex=ax_main)
    ax_y = fig.add_subplot(gs[1:4, 3], sharey=ax_main)

    # --- funzione helper per il 50% HDR ---
    def plot_group(xg, yg, ax, label=None, color=None):
        xy = np.vstack([xg, yg])
        kde = gaussian_kde(xy)
        z = kde(xy)

        # Soglia 50% (highest density region)
        z_sorted = np.sort(z)
        cdf = np.cumsum(z_sorted)
        cdf /= cdf[-1]
        z_50 = z_sorted[np.searchsorted(cdf, 0.5)]

        # Griglia per contour
        xi, yi = np.mgrid[
            params["xlim"][0]:params["xlim"][1]:100j,
            params["ylim"][0]:params["ylim"][1]:100j
        ]
        zi = kde(np.vstack([xi.ravel(), yi.ravel()])).reshape(xi.shape)

        ax.contourf(
            xi, yi, zi,
            levels=[z_50, zi.max()],
            colors=[color if color else params["fill_color"]],
            alpha=params["point_alpha"]
        )
        ax.contour(
            xi, yi, zi,
            levels=[z_50],
            colors=[color if color else params["contour_color"]],
            linewidths=params["contour_width"]
        )
        if label:
            ax.scatter([], [], color=color if color else params["fill_color"],
                       alpha=params["point_alpha"], label=label)

    # --- plot main (eventuale grouping) ---
    if params["group_col"] is not None and params["group_col"] in df.columns:
        import itertools
        colors = itertools.cycle(plt.cm.tab20.colors)
        for name, group in df.groupby(params["group_col"]):
            color = next(colors)
            plot_group(group["pleasantness_score"].values,
                       group["presence_score"].values,
                       ax=ax_main,
                       label=str(name),
                       color=color)
        ax_main.legend(title=params["group_col"])
    else:
        plot_group(x, y, ax=ax_main)

    # --- layout main axis ---
    ax_main.set_xlim(params["xlim"])
    ax_main.set_ylim(params["ylim"])
    ax_main.set_xlabel(params["xlabel"])
    ax_main.set_ylabel(params["ylabel"])

    # Tick locators (major/minor) e griglia con stili diversi
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

    # --- marginali ---
    if params["group_col"] is not None and params["group_col"] in df.columns:
        import itertools
        colors = itertools.cycle(plt.cm.tab20.colors)
        for name, group in df.groupby(params["group_col"]):
            color = next(colors)
            kde_x = gaussian_kde(group["pleasantness_score"].values)
            kde_y = gaussian_kde(group["presence_score"].values)
            xx = np.linspace(params["xlim"][0], params["xlim"][1], params["grid_size"])
            yy = np.linspace(params["ylim"][0], params["ylim"][1], params["grid_size"])
            ax_x.plot(xx, kde_x(xx), color=color,
                      alpha=params["marginal_alpha"],
                      linewidth=params["marginal_linewidth"])
            ax_y.plot(kde_y(yy), yy, color=color,
                      alpha=params["marginal_alpha"],
                      linewidth=params["marginal_linewidth"])
        ax_main.legend(title=params["group_col"])
    else:
        kde_x = gaussian_kde(x)
        kde_y = gaussian_kde(y)
        xx = np.linspace(params["xlim"][0], params["xlim"][1], params["grid_size"])
        yy = np.linspace(params["ylim"][0], params["ylim"][1], params["grid_size"])
        ax_x.plot(xx, kde_x(xx), color=params["marginal_color"],
                  alpha=params["marginal_alpha"],
                  linewidth=params["marginal_linewidth"])
        ax_y.plot(kde_y(yy), yy, color=params["marginal_color"],
                  alpha=params["marginal_alpha"],
                  linewidth=params["marginal_linewidth"])

    # Nasconde assi marginali (solo curve)
    ax_x.axis("off")
    ax_y.axis("off")

    # Layout e salvataggio
    plt.tight_layout()
    if params["savefig"]:
        plt.savefig(params["filename"], dpi=params["dpi"], bbox_inches="tight")
    plt.show()
