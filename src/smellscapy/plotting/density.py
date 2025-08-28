import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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
        "bandwidth": None,  
        "n_levels": 10,


        # Scatter
        "plot_points": True,
        "point_size": 25,
        "point_alpha": 0.8,
        "point_color": "grey",

        # Marginali
        "marginal_color": "navy",
        "marginal_alpha": 0.85,
        "marginal_linewidth": 1.2,
        "grid_size": 200,

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

        # >>> Griglia/ticks <<<
        "xmajor_step": 0.25, "xminor_step": 0.05,
        "ymajor_step": 0.25, "yminor_step": 0.05,
        "grid_major": {"linestyle": "--", "linewidth": 0.9, "alpha": 0.7},
        "grid_minor": {"linestyle": ":",  "linewidth": 0.5, "alpha": 0.35},
        "minor_tick_length": 0,  # 0 = nasconde le tacche minori
        
        # Raggruppamento
        "group_col": None,

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



    # Figura: main + marginali
    fig = plt.figure(figsize=params["figsize"])

    gs = GridSpec(4, 4, figure=fig, wspace=0.05, hspace=0.05)
    ax_main = fig.add_subplot(gs[1:4, 0:3])     # scatter + contour
    ax_top    = fig.add_subplot(gs[0, 0:3], sharex=ax_main)  # marginale X
    ax_right    = fig.add_subplot(gs[1:4, 3], sharey=ax_main)  # marginale Y



    # Scatter
    if params["group_col"] and params["group_col"] in df.columns:
        import itertools
        color_cycle = itertools.cycle(plt.cm.tab20.colors)
        for name, g in df.groupby(params["group_col"]):
            c = next(color_cycle)
            ax_main.scatter(g["pleasantness_score"], g["presence_score"],
                            s=params["point_size"], color=c,
                            alpha=params["point_alpha"], label=str(name))
        ax_main.legend(title=params["group_col"])
    else:
        ax_main.scatter(x, y, s=params["point_size"],
                        color=params["point_color"], alpha=params["point_alpha"])

    # KDE 2D centrale
    if params["group_col"] and params["group_col"] in df.columns:
        import itertools
        color_cycle = itertools.cycle(plt.cm.tab20.colors)
        for name, g in df.groupby(params["group_col"]):
            c = next(color_cycle)
            sns.kdeplot(x=g["pleasantness_score"], y=g["presence_score"], levels=params["n_levels"], fill=True,
                        color=c, alpha=0.9, ax=ax_main, thresh=0.05, label=str(name))
        ax_main.legend(title=params["group_col"])
    else: 
        sns.kdeplot(x=x, y=y, levels=params["n_levels"], fill=True,
                    cmap="Blues", alpha=0.8, ax=ax_main, thresh=0.05)

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


        # --- Marginali 
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
        kde_x = gaussian_kde(x)
        kde_y = gaussian_kde(y)
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
    fig.tight_layout()
    if params["savefig"]:
        fig.savefig(params["filename"], dpi=params["dpi"], bbox_inches="tight")
    plt.show()