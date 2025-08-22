import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from smellscapy.calculations import calculate_pleasantness, calculate_presence


def plot_joint(df, **kwargs):
    # Dizionario dei parametri di default
    params = {
        "xlim": (-1, 1),
        "ylim": (-1, 1),
        "figsize": (8, 8),
        "point_alpha": 0.8,
        "point_color": "grey",
        "xlabel": "Pleasantness",
        "ylabel": "Presence",
        "axis_line_color": "grey",
        "axis_line_style": "--",
        "axis_line_width": 1,
        "contour_alpha": 0.6,
        "contour_color": "black",
        "contour_width": 1,
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
        "filename": "joint_plot.png",
        "dpi": 300,
        "group_col": None
    }

    # Aggiornamento con i kwargs passati dall'utente
    for key, value in kwargs.items():
        if key in params and isinstance(params[key], dict) and isinstance(value, dict):
            params[key].update(value)  # merge dict (es. labels)
        else:
            params[key] = value

    plt.figure(figsize=params["figsize"])

    # Funzione helper per plottare un gruppo
    def plot_group(x, y, label=None, color=None):
        xy = np.vstack([x, y])
        kde = gaussian_kde(xy)
        z = kde(xy)

        # 50% density threshold
        z_sorted = np.sort(z)
        cdf = np.cumsum(z_sorted)
        cdf /= cdf[-1]
        z_50 = z_sorted[np.searchsorted(cdf, 0.5)]

        # Grid
        xi, yi = np.mgrid[
            params["xlim"][0]:params["xlim"][1]:100j,
            params["ylim"][0]:params["ylim"][1]:100j
        ]
        zi = kde(np.vstack([xi.ravel(), yi.ravel()])).reshape(xi.shape)

        # Contour 50° percentile
        plt.contourf(xi, yi, zi, levels=[z_50, zi.max()],
                     colors=[color if color else params["point_color"]],
                     alpha=params["contour_alpha"])
        plt.contour(xi, yi, zi, levels=[z_50],
                    colors=color if color else params["contour_color"],
                    linewidths=params["contour_width"])

        # Scatter
        plt.scatter(x, y, color=color if color else params["point_color"],
                    alpha=params["point_alpha"], label=label)

    # Se c'è suddivisione per gruppi
    if params["group_col"] is not None and params["group_col"] in df.columns:
        import itertools
        colors = itertools.cycle(plt.cm.tab10.colors)
        groups = df.groupby(params["group_col"])
        for name, group in groups:
            color = next(colors)
            plot_group(group['pleasantness_score'].values,
                       group['presence_score'].values,
                       label=str(name),
                       color=color)
        plt.legend(title=params["group_col"])
    else:
        x = df['pleasantness_score'].values
        y = df['presence_score'].values
        plot_group(x, y)

    # Assi e titoli
    plt.xlim(params["xlim"])
    plt.ylim(params["ylim"])
    plt.xlabel(params["xlabel"])
    plt.ylabel(params["ylabel"])
    plt.axhline(0, color=params["axis_line_color"],
                linestyle=params["axis_line_style"],
                linewidth=params["axis_line_width"])
    plt.axvline(0, color=params["axis_line_color"],
                linestyle=params["axis_line_style"],
                linewidth=params["axis_line_width"])

    # Diagonali
    x_vals = np.linspace(params["xlim"][0], params["xlim"][1], 200)
    plt.plot(x_vals, x_vals, linestyle=params["diag_style"],
             color=params["diag_color"], linewidth=params["diag_width"])
    plt.plot(x_vals, -x_vals, linestyle=params["diag_style"],
             color=params["diag_color"], linewidth=params["diag_width"])

    # Etichette
    for lbl in params["labels"].values():
        plt.text(lbl["pos"][0], lbl["pos"][1], lbl["text"],
                 ha='left', va='bottom' if lbl["pos"][1] > 0 else 'top',
                 fontsize=params["fontsize"])

    plt.minorticks_on()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()

    if params["savefig"]:
        plt.savefig(params["filename"], dpi=params["dpi"], bbox_inches='tight')

    plt.show()