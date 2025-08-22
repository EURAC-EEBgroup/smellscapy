import numpy as np
import matplotlib.pyplot as plt
from smellscapy.calculations import calculate_pleasantness, calculate_presence


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
        "line_color": "grey",     #  if no division is performed
        "line_style": "--",
        "line_width": 1,
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

    if params["group_col"] is not None and params["group_col"] in df.columns:
        groups = df.groupby(params["group_col"])
        for name, group in groups:
            plt.scatter(group['pleasantness_score'], group['presence_score'],
                        s=params["point_size"], label=str(name), alpha=0.8)
        plt.legend(title=params["group_col"])
    else:
        plt.scatter(x, y, color=params["point_color"], s=params["point_size"])

    plt.xlim(params["xlim"])
    plt.ylim(params["ylim"])
    plt.xlabel(params["xlabel"])
    plt.ylabel(params["ylabel"])

    # Ortogonal axes layout
    plt.axhline(0, color=params["line_color"], linestyle=params["line_style"], linewidth=params["line_width"])
    plt.axvline(0, color=params["line_color"], linestyle=params["line_style"], linewidth=params["line_width"])

    # Diagonal axes layout
    x_vals = np.linspace(params["xlim"][0], params["xlim"][1], 200)
    plt.plot(x_vals, x_vals, linestyle=params["diag_style"], color=params["diag_color"], linewidth=params["diag_width"])
    plt.plot(x_vals, -x_vals, linestyle=params["diag_style"], color=params["diag_color"], linewidth=params["diag_width"])

    # Diagonal labels
    for lbl in params["labels"].values():
        plt.text(lbl["pos"][0], lbl["pos"][1], lbl["text"], 
                 ha='left', va='bottom' if lbl["pos"][1] > 0 else 'top', 
                 fontsize=params["fontsize"])

    # Grid
    plt.minorticks_on()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()

    # Saving
    if params["savefig"]:
        plt.savefig(params["filename"], dpi=params["dpi"], bbox_inches='tight')

    plt.show()