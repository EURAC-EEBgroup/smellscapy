import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch

import smellscapy.plotting.utils as ut



def plot_simple_density(df, **kwargs):
    """
    Scatter Pleasantness–Presence con:
      - KDE 2D + contorno HDR (50% di default)
      - (opz.) marginali 1D KDE in alto (x) e a destra (y) anche per gruppi

    Richiede colonne:
      - 'pleasantness_score' (x)
      - 'presence_score' (y)
    Opzionale:
      - 'group_by_col' per raggruppare punti, contorni e marginali.
    """

    # ----------------- Parametri -----------------
    params = ut.get_default_plot_params()
    params = ut.update_params(params, **kwargs)

    # ----------------- Figura/Axes -----------------
    show_marginals = bool(params["show_marginals"])
    fig, ax, ax_top, ax_right = ut.create_density_figure(params)
    ax = ut.set_fig_layout(ax, params)

    x = np.asarray(df["pleasantness_score"].values)
    y = np.asarray(df["presence_score"].values)

    # ----------------- Helper KDE -----------------
    nx = ny = int(params["eval_n"])
    xi = np.linspace(params["xlim"][0], params["xlim"][1], nx)
    yi = np.linspace(params["ylim"][0], params["ylim"][1], ny)
    XX, YY = np.meshgrid(xi, yi, indexing="xy")


    group_by_col = params["group_by_col"]
    category_order = params['category_order']
    # ----------------- Disegno 2D (+ marginali se richiesti) -----------------
    if (not group_by_col) or (group_by_col not in df.columns):
        ZZ = ut.kde_on_grid(x, y, XX, YY)
        ax = ut.add_contour_HDR_50(ax, XX, YY, ZZ, params)
       
        if params["show_points"]:
            ax.scatter(x, y, s=params["point_size"], alpha=params["point_alpha"],
                       color=params["point_color"])

        if show_marginals:
            ax_top, ax_right = ut.add_marginals(x, xi, y, yi, ax_top, ax_right, params)

    else:
        if pd.api.types.is_categorical_dtype(df[group_by_col]):
            cats = df[group_by_col].cat
        else:
            cats = df[group_by_col].astype("object").astype("category")

        order = sorted(set(cats))
        if category_order is not None:
            category_order = [x for x in category_order if x in order]
            order = category_order + [x for x in order if x not in category_order]

        color_map = ut.build_categorical_palette(order, params["palette"])

        legend_handles = []
        for cat in order:
            mask = (cats == cat).values
            xc, yc = x[mask], y[mask]

            ZZg = ut.kde_on_grid(xc, yc, XX, YY)
            ax = ut.add_contour_HDR_50(ax, XX, YY, ZZg, params, color_map[cat])

            if params["show_points"]:
                ax.scatter(xc, yc, s=params["point_size"], alpha=params["point_alpha"],
                           color=color_map[cat])

            if show_marginals:
                ax_top, ax_right = ut.add_marginals(xc, xi, yc, yi, ax_top, ax_right, params, color_map[cat])

            legend_handles.append(Patch(facecolor=color_map[cat], edgecolor="none", label=str(cat)))

        if legend_handles:
            ax.legend(handles=legend_handles, title=group_by_col,
                      loc=params["legend_loc"], frameon=True)


    fig.tight_layout()
    plt.show()
    return fig, ax