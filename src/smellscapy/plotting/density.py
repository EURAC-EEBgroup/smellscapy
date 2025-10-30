import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch


import smellscapy.plotting.utils as ut 



def plot_density(df, **kwargs):
    params = ut.get_default_plot_params()
    params['filename'] = "density_plot.png"
    params['fill_alpha'] = 0.9
    params['show_points'] = False
    params = ut.update_params(params, **kwargs)

    # ----------------- Dati -----------------
    x = np.asarray(df["pleasantness_score"].values)
    y = np.asarray(df["presence_score"].values)

    # ----------------- Figura/Axes -----------------
    show_marginals = bool(params["show_marginals"])
    fig, ax, ax_top, ax_right = ut.create_density_figure(params)
    ax = ut.set_fig_layout(ax, params)

    # ----------------- Helper KDE -----------------
    nx = ny = int(params["eval_n"])
    xi = np.linspace(params["xlim"][0], params["xlim"][1], nx)
    yi = np.linspace(params["ylim"][0], params["ylim"][1], ny)
    XX, YY = np.meshgrid(xi, yi, indexing="xy")

    group_by_col = params["group_by_col"]
    category_order = params['category_order']

    # ----------------- Disegno -----------------
    if (not group_by_col) or (group_by_col not in df.columns):
       
        Z = ut.kde_on_grid(x, y, XX, YY)
        ut.draw_contours(
            params,
            ax, XX, YY, Z,
            color="blue" if not params["filled"] else None,
            cmap="Grays" if params["filled"] else None,
            levels=params["levels"],
            filled=params["filled"],
            lw=params["contour_linewidth"],
            alpha=params["fill_alpha"],
        )

        if params["show_points"]:
            ax.scatter(x, y, s=params["point_size"], alpha=params["point_alpha"],
                       color=params["point_color"])

        if show_marginals:
            ax_top, ax_right = ut.add_marginals(x, xi, y, yi, ax_top, ax_right, params)

    else:
        series = df[group_by_col]
        if pd.api.types.is_categorical_dtype(series):
            cats = series.cat
        else:
            cats = series.astype("object").astype("category")

        order = sorted(set(cats))
        if category_order is not None:
            category_order = [x for x in category_order if x in order]
            order = category_order + [x for x in order if x not in category_order]

        color_map = ut.build_categorical_palette(order, params["palette"])

        legend_handles = []
        for cat in order:
            mask = (cats == cat).values
            xc, yc = x[mask], y[mask]

            Zg = ut.kde_on_grid(xc, yc, XX, YY)
            ut.draw_contours(
                params,
                ax, XX, YY, Zg,
                color=color_map[cat],
                cmap=None,
                levels=params["levels"],
                filled=params["filled"],
                lw=params["contour_linewidth"],
                alpha=params["fill_alpha"],
            )

            if params["show_points"]:
                ax.scatter(xc, yc, s=params["point_size"], alpha=params["point_alpha"],
                           color=color_map[cat])
                
            if show_marginals:
                ax_top, ax_right = ut.add_marginals(xc, xi, yc, yi, ax_top, ax_right, params, color_map[cat])

            legend_handles.append(Patch(facecolor=color_map[cat] if params["filled"] else "none",
                                        edgecolor=color_map[cat], label=str(cat)))

        if legend_handles:
            ax.legend(handles=legend_handles, title=group_by_col,
                      loc=params["legend_loc"], frameon=True)


    fig.tight_layout()
    plt.show()
    return fig, ax