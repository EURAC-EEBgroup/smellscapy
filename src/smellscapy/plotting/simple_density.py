import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib.gridspec import GridSpec
from smellscapy.calculations import calculate_pleasantness, calculate_presence


def plot_simple_density(df, **kwargs):
    # Default parameters
    params = {
        "xlim": (-1, 1),
        "ylim": (-1, 1),
        "figsize": (8, 8),
        "xlabel": "Pleasantness",
        "ylabel": "Presence",
        "point_alpha": 0.6,
        "contour_color": "black",
        "contour_width": 1,
        "fill_color": "grey",
        "axis_line_color": "grey",
        "axis_line_style": "--",
        "axis_line_width": 1,
        "diag_color": "black",
        "diag_style": "--",
        "diag_width": 0.8,
        "labels": {
            "overpowering": {"pos": (-0.6, 0.5), "text": "Overpowering"},
            "detached": {"pos": (-0.6, -0.5), "text": "Detached"},
            "engaging": {"pos": (0.4, 0.5), "text": "Engaging"},
            "light": {"pos": (0.4, -0.5), "text": "Light"},
        },
        "fontsize": 10,
        "savefig": True,
        "filename": "simple_density_plot.png",
        "dpi": 300,
        "group_col": None,   # colonna per eventuale split
        # nuovi parametri per marginali
        "marginal_color": "black",
        "marginal_alpha": 0.8,
        "marginal_linewidth": 1.2,
        "grid_size": 200
    }

    # Update solo con kwargs
    for key, value in kwargs.items():
        if key in params and isinstance(params[key], dict) and isinstance(value, dict):
            params[key].update(value)
        else:
            params[key] = value

    # Estrai i dati
    x = df['pleasantness_score'].values
    y = df['presence_score'].values

    # Griglia figure
    fig = plt.figure(figsize=params["figsize"])
    gs = GridSpec(4, 4, figure=fig, wspace=0.05, hspace=0.05)

    ax_main = fig.add_subplot(gs[1:4, 0:3])
    ax_x = fig.add_subplot(gs[0, 0:3], sharex=ax_main)
    ax_y = fig.add_subplot(gs[1:4, 3], sharey=ax_main)

    # funzione per il contour 50%
    def plot_group(x, y, ax, label=None, color=None):
        xy = np.vstack([x, y])
        kde = gaussian_kde(xy)
        z = kde(xy)

        # Threshold 50%
        z_sorted = np.sort(z)
        cdf = np.cumsum(z_sorted)
        cdf /= cdf[-1]
        z_50 = z_sorted[np.searchsorted(cdf, 0.5)]

        # Grid for contour
        xi, yi = np.mgrid[
            params["xlim"][0]:params["xlim"][1]:100j,
            params["ylim"][0]:params["ylim"][1]:100j
        ]
        zi = kde(np.vstack([xi.ravel(), yi.ravel()])).reshape(xi.shape)

        ax.contourf(xi, yi, zi, levels=[z_50, zi.max()],
                     colors=[color if color else params["fill_color"]],
                     alpha=params["point_alpha"])
        ax.contour(xi, yi, zi, levels=[z_50],
                    colors=[color if color else params["contour_color"]],
                    linewidths=params["contour_width"])
        if label:
            ax.scatter([], [], color=color if color else params["fill_color"],
                        alpha=params["point_alpha"], label=label)

    # Plot (main)
    if params["group_col"] is not None and params["group_col"] in df.columns:
        import itertools
        colors = itertools.cycle(plt.cm.tab10.colors)
        groups = df.groupby(params["group_col"])
        for name, group in groups:
            color = next(colors)
            plot_group(group['pleasantness_score'].values,
                       group['presence_score'].values,
                       ax=ax_main,
                       label=str(name),
                       color=color)
        ax_main.legend(title=params["group_col"])
    else:
        plot_group(x, y, ax=ax_main)

    # Layout del main plot
    ax_main.set_xlim(params["xlim"])
    ax_main.set_ylim(params["ylim"])
    ax_main.set_xlabel(params["xlabel"])
    ax_main.set_ylabel(params["ylabel"])

    # Assi centrali
    ax_main.axhline(0, color=params["axis_line_color"],
                linestyle=params["axis_line_style"],
                linewidth=params["axis_line_width"])
    ax_main.axvline(0, color=params["axis_line_color"],
                linestyle=params["axis_line_style"],
                linewidth=params["axis_line_width"])

    # Diagonal lines
    x_vals = np.linspace(params["xlim"][0], params["xlim"][1], 200)
    ax_main.plot(x_vals, x_vals, linestyle=params["diag_style"],
             color=params["diag_color"], linewidth=params["diag_width"])
    ax_main.plot(x_vals, -x_vals, linestyle=params["diag_style"],
             color=params["diag_color"], linewidth=params["diag_width"])

    # Diagonal labels
    for lbl in params["labels"].values():
        ax_main.text(lbl["pos"][0], lbl["pos"][1], lbl["text"],
                 ha='left', va='bottom' if lbl["pos"][1] > 0 else 'top',
                 fontsize=params["fontsize"])

    # Griglia main
    ax_main.minorticks_on()
    ax_main.grid(True, which='both', linestyle='--', linewidth=0.5)

    # === Marginali ===
    kde_x = gaussian_kde(x)
    kde_y = gaussian_kde(y)
    xx = np.linspace(params["xlim"][0], params["xlim"][1], params["grid_size"])
    yy = np.linspace(params["ylim"][0], params["ylim"][1], params["grid_size"])
    pdf_x = kde_x(xx)
    pdf_y = kde_y(yy)

    ax_x.plot(xx, pdf_x, color=params["marginal_color"],
              alpha=params["marginal_alpha"],
              linewidth=params["marginal_linewidth"])
    ax_x.axis("off")

    ax_y.plot(pdf_y, yy, color=params["marginal_color"],
              alpha=params["marginal_alpha"],
              linewidth=params["marginal_linewidth"])
    ax_y.axis("off")

    plt.tight_layout()

    if params["savefig"]:
        plt.savefig(params["filename"], dpi=params["dpi"], bbox_inches='tight')

    plt.show()