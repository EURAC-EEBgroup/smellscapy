import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
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
        "group_col": None   # column used to divide the dataset
    }


    # Update only the parameters provided by the user
    for key, value in kwargs.items():
        if key in params and isinstance(params[key], dict) and isinstance(value, dict):
            params[key].update(value)
        else:
            params[key] = value
    
    x = df['pleasantness_score'].values
    y = df['presence_score'].values

    plt.figure(figsize=params["figsize"])

    # calculate and plot 50% contour
    def plot_group(x, y, label=None, color=None):
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

        plt.contourf(xi, yi, zi, levels=[z_50, zi.max()],
                     colors=[color if color else params["fill_color"]],
                     alpha=params["point_alpha"])
        plt.contour(xi, yi, zi, levels=[z_50],
                    colors=[color if color else params["contour_color"]],
                    linewidths=params["contour_width"])
        if label:
            plt.scatter([], [], color=color if color else params["fill_color"],
                        alpha=params["point_alpha"], label=label)

    # Plot
    if params["group_col"] is not None and params["group_col"] in df.columns:
        import itertools
        colors = itertools.cycle(plt.cm.tab10.colors)  # palette di default
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

    plt.xlim(params["xlim"])
    plt.ylim(params["ylim"])
    plt.xlabel(params["xlabel"])
    plt.ylabel(params["ylabel"])

    # Central axes
    plt.axhline(0, color=params["axis_line_color"], linestyle=params["axis_line_style"], linewidth=params["axis_line_width"])
    plt.axvline(0, color=params["axis_line_color"], linestyle=params["axis_line_style"], linewidth=params["axis_line_width"])

    # Diagonal lines
    x_vals = np.linspace(params["xlim"][0], params["xlim"][1], 200)
    plt.plot(x_vals, x_vals, linestyle=params["diag_style"], color=params["diag_color"], linewidth=params["diag_width"])
    plt.plot(x_vals, -x_vals, linestyle=params["diag_style"], color=params["diag_color"], linewidth=params["diag_width"])

    # Diagonal labels
    for lbl in params["labels"].values():
        plt.text(lbl["pos"][0], lbl["pos"][1], lbl["text"],
                 ha='left', va='bottom' if lbl["pos"][1] > 0 else 'top',
                 fontsize=params["fontsize"])

    # Grid and formatting
    plt.minorticks_on()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()

    if params["savefig"]:
        plt.savefig(params["filename"], dpi=params["dpi"], bbox_inches='tight')

    plt.show()