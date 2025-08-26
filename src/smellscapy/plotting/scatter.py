import numpy as np
import matplotlib.pyplot as plt
from smellscapy.calculations import calculate_pleasantness, calculate_presence
from matplotlib.ticker import MultipleLocator


def plot_scatter(df, **kwargs):

    # Default values dictianary
    params = {
        "xlim": (-1, 1),
        "ylim": (-1, 1),
        "figsize": (8, 8),
        "point_color": "grey",
        "point_size": 50,
        "xlabel": "Pleasantness",
        "ylabel": "Presence",
        "line_color": "grey",
        "line_style" : "-",
        "line_width" : 0.5,
        "xmajor_step": 0.25, "xminor_step": 0.05,
        "ymajor_step": 0.25, "yminor_step": 0.05,
        "grid_major": {"linestyle": "--", "linewidth": 0.8, "alpha": 0.7},
        "grid_minor": {"linestyle": ":",  "linewidth": 0.5, "alpha": 0.35},
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
        "savefig": True,
        "filename": "scatter_plot.png",
        "dpi": 300,
        "group_col": None   # column used to divide the dataset. Default is no division
    }

# Update only the parameters provided by the user
    for key, value in kwargs.items():
        if key in params and isinstance(params[key], dict) and isinstance(value, dict):
            params[key].update(value)
        else:
            params[key] = value

    # Calculate coordinates
    x = df['pleasantness_score'].values
    y = df['presence_score'].values

    # Plot
    plt.figure(figsize=params["figsize"])


    ax = plt.gca()

    ax.set_xlim(params["xlim"])
    ax.set_ylim(params["ylim"])
    ax.set_xlabel(params["xlabel"])
    ax.set_ylabel(params["ylabel"])

    # Locator: passi diversi per ticks maggiori e minori
    ax.xaxis.set_major_locator(MultipleLocator(params["xmajor_step"]))
    ax.xaxis.set_minor_locator(MultipleLocator(params["xminor_step"]))
    ax.yaxis.set_major_locator(MultipleLocator(params["ymajor_step"]))
    ax.yaxis.set_minor_locator(MultipleLocator(params["yminor_step"]))

    # Metti la griglia sotto i punti
    ax.set_axisbelow(True)

    # Griglia: stili diversi per major/minor
    ax.grid(True, which="major", **params["grid_major"])
    ax.grid(True, which="minor", **params["grid_minor"])

    # (opzionale) niente “tacchette” visive per i minor ticks
    ax.tick_params(which="minor", length=0)

    # Assi ortogonali e diagonali (come avevi)
    ax.axhline(0, color=params["line_color"], linestyle=params["line_style"], linewidth=params["line_width"])
    ax.axvline(0, color=params["line_color"], linestyle=params["line_style"], linewidth=params["line_width"])

    x_vals = np.linspace(params["xlim"][0], params["xlim"][1], 200)
    ax.plot(x_vals,  x_vals, linestyle=params["diag_style"], color=params["diag_color"], linewidth=params["diag_width"])
    ax.plot(x_vals, -x_vals, linestyle=params["diag_style"], color=params["diag_color"], linewidth=params["diag_width"])


    # Etichette dei quadranti
    for lbl in params["labels"].values():
        ax.text(lbl["pos"][0], lbl["pos"][1], lbl["text"],
                ha="center", va="center", **params["labels_style"])

    if params["group_col"] is not None and params["group_col"] in df.columns:
        groups = df.groupby(params["group_col"])
        for name, group in groups:
            plt.scatter(group['pleasantness_score'], group['presence_score'],
                        s=params["point_size"], label=str(name), alpha=0.8)
        plt.legend(title=params["group_col"])
    else:
        plt.scatter(x, y, color=params["point_color"], s=params["point_size"])

    # Saving
    if params["savefig"]:
        plt.savefig(params["filename"], dpi=params["dpi"], bbox_inches='tight')

    plt.show()