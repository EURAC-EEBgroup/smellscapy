import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import gaussian_kde
from smellscapy.calculations import calculate_pleasantness, calculate_presence
from matplotlib.ticker import MultipleLocator
from matplotlib.gridspec import GridSpec
import matplotlib as mpl
from matplotlib.patches import Patch


def plot_simple_density(df, **kwargs):
    """
    Scatter Pleasantness–Presence con:
      - KDE 2D + contorno HDR (50% di default)
      - (opz.) marginali 1D KDE in alto (x) e a destra (y) anche per gruppi

    Richiede colonne:
      - 'pleasantness_score' (x)
      - 'presence_score' (y)
    Opzionale:
      - 'group_col' (alias 'color_by') per raggruppare punti, contorni e marginali.
    """

    # ----------------- Parametri -----------------
    params = {
        "xlim": (-1, 1),
        "ylim": (-1, 1),
        "figsize": (8, 8),
        "xlabel": "Pleasantness",
        "ylabel": "Presence",

        # Contorni KDE 2D
        "contour_color": "black",
        "contour_width": 1.0,
        "fill_color": "grey",
        "fill_alpha": 0.4,

        # Assi centrali
        "axis_line_color": "grey",
        "axis_line_style": "-",
        "axis_line_width": 0.8,

        # Diagonali
        "diag_color": "grey",
        "diag_style": "--",
        "diag_width": 0.7,

        # Griglia/ticks
        "xmajor_step": 0.25, "xminor_step": 0.05,
        "ymajor_step": 0.25, "yminor_step": 0.05,
        "grid_major": {"linestyle": "--", "linewidth": 0.8, "alpha": 0.7},
        "grid_minor": {"linestyle": ":",  "linewidth": 0.5, "alpha": 0.35},
        "minor_tick_length": 0,

        # Griglia KDE 2D
        "eval_n": 300,
        "hdr_p": 0.5,

        # Scatter
        "show_points": True,
        "point_size": 50,
        "point_alpha": 0.25,
        "point_color": "grey",

        # Raggruppamento/colori
        "group_col": None,
        "color_by": None,   # alias
        "palette": None,
        "legend_loc": "upper left",
        "category_order": None,

        # Etichette quadranti
        "show_quadrant_labels": True,
        "labels": {
            "overpowering": {"pos": (-0.5,  0.5), "text": "Overpowering"},
            "detached":     {"pos": (-0.5, -0.5), "text": "Detached"},
            "engaging":     {"pos": ( 0.5,  0.5), "text": "Engaging"},
            "light":        {"pos": ( 0.5, -0.5), "text": "Light"},
        },
        "labels_style": {"fontsize": 10, "fontstyle": "italic", "alpha": 0.7},

        # --- Marginali 1D ---
        "show_marginals": True,
        "marginal_height_ratio": 1.0,  # altezza (top) e larghezza (right) relative
        "marginal_linewidth": 1.0,
        "marginal_fill_alpha": 0.15,
        "marginal_bw": None,           # banda KDE 1D
    }

    # Override con kwargs
    for k, v in kwargs.items():
        if k in params and isinstance(params[k], dict) and isinstance(v, dict):
            params[k].update(v)
        else:
            params[k] = v

    # Alias group_col
    if params.get("group_col") is None and params.get("color_by") is not None:
        params["group_col"] = params["color_by"]

    # ----------------- Dati -----------------
    if ("pleasantness_score" not in df.columns) or ("presence_score" not in df.columns):
        raise ValueError("Colonne richieste: 'pleasantness_score' e 'presence_score'.")

    x = np.asarray(df["pleasantness_score"].values)
    y = np.asarray(df["presence_score"].values)

    # ----------------- Figura/Axes -----------------
    show_marginals = bool(params["show_marginals"])
    if show_marginals:
        fig = plt.figure(figsize=params["figsize"])
        gs = fig.add_gridspec(
            nrows=2, ncols=2,
            width_ratios=[4, params["marginal_height_ratio"]],
            height_ratios=[params["marginal_height_ratio"], 4],
            hspace=0.04, wspace=0.04
        )
        ax_top = fig.add_subplot(gs[0, 0])
        ax = fig.add_subplot(gs[1, 0], sharex=ax_top)
        ax_right = fig.add_subplot(gs[1, 1], sharey=ax)
    else:
        fig, ax = plt.subplots(figsize=params["figsize"])
        ax_top = None
        ax_right = None

    # ----------------- Helper KDE -----------------
    nx = ny = int(params["eval_n"])
    xi = np.linspace(params["xlim"][0], params["xlim"][1], nx)
    yi = np.linspace(params["ylim"][0], params["ylim"][1], ny)
    XX, YY = np.meshgrid(xi, yi, indexing="xy")

    def kde_on_grid(x_sub, y_sub):
        if len(x_sub) < 3:
            return None
        kde = gaussian_kde(np.vstack([x_sub, y_sub]))
        ZZ = kde(np.vstack([XX.ravel(), YY.ravel()])).reshape(YY.shape)
        return ZZ

    def hdr_threshold_from_grid(zi, p, xlim, ylim):
        ny_, nx_ = zi.shape
        dx = (xlim[1] - xlim[0]) / (nx_ - 1)
        dy = (ylim[1] - ylim[0]) / (ny_ - 1)
        cell_area = dx * dy
        zflat = zi.ravel()
        order = np.argsort(zflat)[::-1]
        zsorted = zflat[order]
        cum_mass = np.cumsum(zsorted * cell_area)
        target = p * cum_mass[-1]
        idx = np.searchsorted(cum_mass, target)
        idx = min(idx, zsorted.size - 1)
        return zsorted[idx], float(np.max(zi))

    def kde1d(values, grid, bw=None):
        vals = np.asarray(values)
        vals = vals[np.isfinite(vals)]
        if vals.size < 3:
            return None
        kde = gaussian_kde(vals, bw_method=bw)
        return kde(grid)

    def build_categorical_palette(categories, palette_param):
        if isinstance(palette_param, dict):
            return {c: palette_param.get(c, "grey") for c in categories}
        if isinstance(palette_param, str) and (palette_param in mpl.colormaps):
            cmap = mpl.colormaps[palette_param]
            return {c: cmap(i / max(1, len(categories)-1)) for i, c in enumerate(categories)}
        if isinstance(palette_param, (list, tuple)):
            colors = list(palette_param)
            if len(colors) < len(categories):
                m = int(np.ceil(len(categories)/len(colors)))
                colors = (colors * m)[:len(categories)]
            return {c: col for c, col in zip(categories, colors)}
        cmap = mpl.colormaps.get("tab10")
        return {c: cmap(i % 10) for i, c in enumerate(categories)}

    group_col = params["group_col"]

    # ----------------- Disegno 2D (+ marginali se richiesti) -----------------
    if (not group_col) or (group_col not in df.columns):
        ZZ = kde_on_grid(x, y)
        if ZZ is not None:
            thr, zmax = hdr_threshold_from_grid(ZZ, params["hdr_p"], params["xlim"], params["ylim"])
            if thr < zmax:
                ax.contourf(XX, YY, ZZ, levels=[thr, zmax],
                            colors=[params["fill_color"]], alpha=params["fill_alpha"])
                ax.contour(XX, YY, ZZ, levels=[thr],
                           colors=[params["contour_color"]], linewidths=params["contour_width"])
        if params["show_points"]:
            ax.scatter(x, y, s=params["point_size"], alpha=params["point_alpha"],
                       color=params["point_color"])

        if show_marginals:
            fx = kde1d(x, xi, bw=params["marginal_bw"])
            if fx is not None:
                ax_top.fill_between(xi, 0, fx, alpha=params["marginal_fill_alpha"], color=params["fill_color"])
                ax_top.plot(xi, fx, linewidth=params["marginal_linewidth"], color=params["contour_color"])
            fy = kde1d(y, yi, bw=params["marginal_bw"])
            if fy is not None:
                ax_right.fill_betweenx(yi, 0, fy, alpha=params["marginal_fill_alpha"], color=params["fill_color"])
                ax_right.plot(fy, yi, linewidth=params["marginal_linewidth"], color=params["contour_color"])

    else:
        series = df[group_col]
        # No binning. Gestione NA sicura.
        if pd.api.types.is_categorical_dtype(series):
            cats = series.cat.add_categories(["NA"]).fillna("NA")
        else:
            cats = series.astype("object").fillna("NA").astype("category")

        # Ordine categorie
        if params.get("category_order") is not None:
            order = [c for c in params["category_order"] if c in cats.cat.categories]
            order += [c for c in cats.cat.categories if c not in order]
        else:
            order = sorted(cats.cat.categories)

        cats = cats.cat.reorder_categories(order, ordered=True)
        color_map = build_categorical_palette(order, params["palette"])

        legend_handles = []
        for cat in order:
            mask = (cats == cat).values
            if not np.any(mask):
                continue
            xc, yc = x[mask], y[mask]

            ZZg = kde_on_grid(xc, yc)
            if ZZg is not None:
                thr_g, zmax_g = hdr_threshold_from_grid(ZZg, params["hdr_p"], params["xlim"], params["ylim"])
                if thr_g < zmax_g:
                    ax.contourf(XX, YY, ZZg, levels=[thr_g, zmax_g],
                                colors=[color_map[cat]], alpha=params["fill_alpha"])
                    ax.contour(XX, YY, ZZg, levels=[thr_g],
                               colors=[color_map[cat]], linewidths=params["contour_width"])

            if params["show_points"]:
                ax.scatter(xc, yc, s=params["point_size"], alpha=params["point_alpha"],
                           color=color_map[cat])

            if show_marginals:
                fx = kde1d(xc, xi, bw=params["marginal_bw"])
                if fx is not None:
                    ax_top.fill_between(xi, 0, fx, alpha=params["marginal_fill_alpha"], color=color_map[cat])
                    ax_top.plot(xi, fx, linewidth=params["marginal_linewidth"], color=color_map[cat])

                fy = kde1d(yc, yi, bw=params["marginal_bw"])
                if fy is not None:
                    ax_right.fill_betweenx(yi, 0, fy, alpha=params["marginal_fill_alpha"], color=color_map[cat])
                    ax_right.plot(fy, yi, linewidth=params["marginal_linewidth"], color=color_map[cat])

            legend_handles.append(Patch(facecolor=color_map[cat], edgecolor="none", label=str(cat)))

        if legend_handles:
            ax.legend(handles=legend_handles, title=group_col,
                      loc=params["legend_loc"], frameon=True)

    # ----------------- Layout / assi / griglia -----------------
    ax.set_xlim(params["xlim"]); ax.set_ylim(params["ylim"])
    ax.set_xlabel(params["xlabel"]); ax.set_ylabel(params["ylabel"])

    ax.xaxis.set_major_locator(MultipleLocator(params["xmajor_step"]))
    ax.xaxis.set_minor_locator(MultipleLocator(params["xminor_step"]))
    ax.yaxis.set_major_locator(MultipleLocator(params["ymajor_step"]))
    ax.yaxis.set_minor_locator(MultipleLocator(params["yminor_step"]))
    ax.set_axisbelow(True)
    ax.grid(True, which="major", **params["grid_major"])
    ax.grid(True, which="minor", **params["grid_minor"])
    ax.tick_params(which="minor", length=params["minor_tick_length"])

    # Assi centrali + diagonali
    ax.axhline(0, color=params["axis_line_color"],
               linestyle=params["axis_line_style"], linewidth=params["axis_line_width"])
    ax.axvline(0, color=params["axis_line_color"],
               linestyle=params["axis_line_style"], linewidth=params["axis_line_width"])
    xv = np.linspace(params["xlim"][0], params["xlim"][1], 200)
    ax.plot(xv,  xv, linestyle=params["diag_style"],
            color=params["diag_color"], linewidth=params["diag_width"])
    ax.plot(xv, -xv, linestyle=params["diag_style"],
            color=params["diag_color"], linewidth=params["diag_width"])

    # Pulizia marginali (solo se presenti)
    if show_marginals:
        # minimal/clean: niente assi/ticks/bordi
        ax_top.set_xlim(params["xlim"]); ax_top.axis("off")
        ax_right.set_ylim(params["ylim"]); ax_right.axis("off")
    
    #etichette dei quadranti
    for lbl in params["labels"].values():
        ax.text(lbl["pos"][0], lbl["pos"][1], lbl["text"],
                ha="center", va="center", **params["labels_style"])

    fig.tight_layout()
    plt.show()
    return fig, ax