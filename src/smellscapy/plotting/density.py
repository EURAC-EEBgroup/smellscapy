import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import MultipleLocator
from smellscapy.calculations import calculate_pleasantness, calculate_presence

def plot_density(df, **kwargs):
    # Parametri di default
    params = {
        "figsize": (8, 8),
        "xlim": (-1, 1),
        "ylim": (-1, 1),
        "xlabel": "Pleasantness",
        "ylabel": "Presence",

        # KDE
        "grid_size": 200,
        "bandwidth": None,     # passa numeri tipo 0.2 per fissare la bw
        "n_levels": 15,

        # Colori/contour
        "cmap": "Blues",
        "contour_alpha": 0.8,
        "line_color": "black",
        "line_width": 0.5,

        # Scatter
        "plot_points": True,
        "point_size": 25,
        "point_alpha": 0.5,
        "point_color": "grey",

        # Marginali
        "marginal_color": "black",
        "marginal_alpha": 0.8,
        "marginal_linewidth": 1.2,

        # Assi
        "axis_line_color": "grey",
        "axis_line_style": "-",
        "axis_line_width": 0.5,
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

        # >>> Griglia/ticks (NUOVO) <<<
        "xmajor_step": 0.25, "xminor_step": 0.05,
        "ymajor_step": 0.25, "yminor_step": 0.05,
        "grid_major": {"linestyle": "--", "linewidth": 0.9, "alpha": 0.7},
        "grid_minor": {"linestyle": ":",  "linewidth": 0.5, "alpha": 0.35},
        "minor_tick_length": 0,  # 0 = nasconde le tacche minori

        # Output
        "savefig": True,
        "filename": "density.png",
        "dpi": 300,
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
    xy = np.vstack([x, y])

    # KDE 2D
    kde2d = gaussian_kde(xy, bw_method=params["bandwidth"])
    xi, yi = np.mgrid[
        params["xlim"][0]:params["xlim"][1]:complex(params["grid_size"]),
        params["ylim"][0]:params["ylim"][1]:complex(params["grid_size"])
    ]
    zi = kde2d(np.vstack([xi.ravel(), yi.ravel()])).reshape(xi.shape)

    # KDE 1D
    kde_x = gaussian_kde(x, bw_method=params["bandwidth"])
    kde_y = gaussian_kde(y, bw_method=params["bandwidth"])
    xx = np.linspace(params["xlim"][0], params["xlim"][1], params["grid_size"])
    yy = np.linspace(params["ylim"][0], params["ylim"][1], params["grid_size"])
    pdf_x = kde_x(xx)
    pdf_y = kde_y(yy)

    # Figura: main + marginali
    fig = plt.figure(figsize=params["figsize"])
    gs = GridSpec(4, 4, figure=fig, wspace=0.05, hspace=0.05)
    ax_main = fig.add_subplot(gs[1:4, 0:3])     # scatter + contour
    ax_x    = fig.add_subplot(gs[0, 0:3], sharex=ax_main)  # marginale X
    ax_y    = fig.add_subplot(gs[1:4, 3], sharey=ax_main)  # marginale Y

    # Contour centrale
    cf = ax_main.contourf(
        xi, yi, zi,
        levels=params["n_levels"],
        cmap=params["cmap"],
        alpha=params["contour_alpha"]
    )
    ax_main.contour(
        xi, yi, zi,
        levels=params["n_levels"],
        colors=params["line_color"],
        linewidths=params["line_width"]
    )

    # Scatter opzionale
    if params["plot_points"]:
        ax_main.scatter(x, y,
                        s=params["point_size"],
                        alpha=params["point_alpha"],
                        color=params["point_color"])

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

    # Etichette diagonali
    for lbl in params["labels"].values():
        ax_main.text(lbl["pos"][0], lbl["pos"][1], lbl["text"],
                     ha="left",
                     va="bottom" if lbl["pos"][1] > 0 else "top",
                     **params["labels_style"])

    # >>> Griglia distinta major/minor <<<
    ax_main.xaxis.set_major_locator(MultipleLocator(params["xmajor_step"]))
    ax_main.xaxis.set_minor_locator(MultipleLocator(params["xminor_step"]))
    ax_main.yaxis.set_major_locator(MultipleLocator(params["ymajor_step"]))
    ax_main.yaxis.set_minor_locator(MultipleLocator(params["yminor_step"]))
    ax_main.set_axisbelow(True)
    ax_main.grid(True, which="major", **params["grid_major"])
    ax_main.grid(True, which="minor", **params["grid_minor"])
    ax_main.tick_params(which="minor", length=params["minor_tick_length"])

    # Limiti ed etichette
    ax_main.set_xlim(params["xlim"])
    ax_main.set_ylim(params["ylim"])
    ax_main.set_xlabel(params["xlabel"])
    ax_main.set_ylabel(params["ylabel"])

    # Marginale X
    ax_x.plot(xx, pdf_x,
              color=params["marginal_color"],
              alpha=params["marginal_alpha"],
              linewidth=params["marginal_linewidth"])
    ax_x.axis("off")

    # Marginale Y
    ax_y.plot(pdf_y, yy,
              color=params["marginal_color"],
              alpha=params["marginal_alpha"],
              linewidth=params["marginal_linewidth"])
    ax_y.axis("off")

    # Layout e salvataggio
    fig.tight_layout()
    if params["savefig"]:
        fig.savefig(params["filename"], dpi=params["dpi"], bbox_inches="tight")
    plt.show()