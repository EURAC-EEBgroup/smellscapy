import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import gaussian_kde
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import MultipleLocator
from matplotlib.patches import Patch
import matplotlib as mpl
from smellscapy.calculations import calculate_pleasantness, calculate_presence

def plot_density(df, **kwargs):
    params = {
        "xlim": (-1, 1),
        "ylim": (-1, 1),
        "figsize": (8, 8),
        "xlabel": "Pleasantness",
        "ylabel": "Presence",

        # Contorni KDE 2D
        "levels": 10,             # int (numero livelli) o array di livelli-bordo
        "filled": True,           # True -> contourf, False -> contour
        "extend": "max",          # 'neither' | 'min' | 'max' | 'both'
        "contour_linewidth": 0.05,
        "fill_alpha": 1,

        # Esclusione estremi inferiori
        "skip_low_levels": 1,     # quante bande escludere dal basso (0 = nessuna)
        "min_frac": None,         # se float (0–1), esclude tutto sotto min_frac * Z.max()

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

        # Scatter
        "show_points": False,
        "point_size": 50,
        "point_alpha": 0.25,
        "point_color": "grey",

        # Raggruppamento/colori
        "group_col": None,
        "color_by": None,     # alias
        "palette": None,      # dict | nome cmap | lista
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
        "marginal_height_ratio": 1.0,
        "marginal_linewidth": 1,
        "marginal_fill_alpha": 0,
        "marginal_bw": None,  # banda KDE 1D
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
    req = ("pleasantness_score" in df.columns) and ("presence_score" in df.columns)
    if not req:
        raise ValueError("Servono le colonne 'pleasantness_score' e 'presence_score'.")
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

    def kde2d_on_grid(x_sub, y_sub):
        vals_x = np.asarray(x_sub); vals_y = np.asarray(y_sub)
        mask = np.isfinite(vals_x) & np.isfinite(vals_y)
        vals_x, vals_y = vals_x[mask], vals_y[mask]
        if vals_x.size < 3:  # n>d
            return None
        kde = gaussian_kde(np.vstack([vals_x, vals_y]))
        ZZ = kde(np.vstack([XX.ravel(), YY.ravel()])).reshape(YY.shape)
        return ZZ

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

    # --------- MODIFICA: livelli con esclusione estremi inferiori ----------
    def _compute_levels_from_int(Z, n_levels, skip_low, min_frac):
        zmin, zmax = float(np.nanmin(Z)), float(np.nanmax(Z))
        if not np.isfinite(zmin) or not np.isfinite(zmax) or zmax <= zmin:
            return None
        # livelli-bordo uniformi su [zmin, zmax]
        levs_all = np.linspace(zmin, zmax, n_levels + 1)

        # priorità a min_frac
        if isinstance(min_frac, (int, float)) and (min_frac is not None):
            thr = zmax * float(min_frac)
            levs = levs_all[levs_all >= thr]
            # garantisci almeno 2 bordi
            if levs.size < 2:
                levs = levs_all[-2:]
            return levs

        # altrimenti salta 'skip_low' bande
        skip = int(max(0, skip_low))
        levs = levs_all[skip:]
        if levs.size < 2:
            levs = levs_all[-2:]
        return levs

    def draw_contours(ax_, XX, YY, Z, color=None, cmap=None, levels=5, filled=False, lw=1, alpha=1):
        if Z is None:
            return

        if isinstance(levels, int):
            levs = _compute_levels_from_int(
                Z, levels,
                skip_low=params.get("skip_low_levels", 0),
                min_frac=params.get("min_frac", None),
            )
            if levs is None:
                return
        else:
            levs = np.asarray(levels)
            # applica min_frac anche a livelli espliciti, se richiesto
            mf = params.get("min_frac", None)
            if isinstance(mf, (int, float)):
                zmax = float(np.nanmax(Z))
                levs = levs[levs >= zmax * float(mf)]
            # in alternativa, salta le prime 'skip_low_levels' bande
            else:
                k = int(max(0, params.get("skip_low_levels", 0)))
                if k > 0 and levs.size > k:
                    levs = levs[k:]

            if levs.size < 2:
                return

        if filled:
            if cmap is None and color is not None:
                rgba = mpl.colors.to_rgba(color)
                cmap = mpl.colors.LinearSegmentedColormap.from_list(
                    "", [(1, 1, 1, 0), (rgba[0], rgba[1], rgba[2], alpha)]
                )
            ax_.contourf(XX, YY, Z, levels=levs, cmap=cmap, alpha=alpha,
                         extend=params["extend"], antialiased=True)
            ax_.contour(XX, YY, Z, levels=levs, colors=[color] if color else None, linewidths=lw*0.8)
        else:
            ax_.contour(XX, YY, Z, levels=levs, colors=[color] if color else None, linewidths=lw)

    group_col = params["group_col"]

    # ----------------- Disegno -----------------
    if (not group_col) or (group_col not in df.columns):
        Z = kde2d_on_grid(x, y)
        draw_contours(
            ax, XX, YY, Z,
            color="black" if not params["filled"] else None,
            cmap="Greys" if params["filled"] else None,
            levels=params["levels"],
            filled=params["filled"],
            lw=params["contour_linewidth"],
            alpha=params["fill_alpha"],
        )
        if params["show_points"]:
            ax.scatter(x, y, s=params["point_size"], alpha=params["point_alpha"],
                       color=params["point_color"])

        if show_marginals:
            fx = kde1d(x, xi, bw=params["marginal_bw"])
            if fx is not None:
                ax_top.fill_between(xi, 0, fx, alpha=params["marginal_fill_alpha"], color="grey")
                ax_top.plot(xi, fx, linewidth=params["marginal_linewidth"], color="black")
            fy = kde1d(y, yi, bw=params["marginal_bw"])
            if fy is not None:
                ax_right.fill_betweenx(yi, 0, fy, alpha=params["marginal_fill_alpha"], color="grey")
                ax_right.plot(fy, yi, linewidth=params["marginal_linewidth"], color="black")

    else:
        series = df[group_col]
        if pd.api.types.is_categorical_dtype(series):
            cats = series.cat.add_categories(["NA"]).fillna("NA")
        else:
            cats = series.astype("object").fillna("NA").astype("category")

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

            Zg = kde2d_on_grid(xc, yc)
            draw_contours(
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
                fx = kde1d(xc, xi, bw=params["marginal_bw"])
                if fx is not None:
                    ax_top.fill_between(xi, 0, fx, alpha=params["marginal_fill_alpha"], color=color_map[cat])
                    ax_top.plot(xi, fx, linewidth=params["marginal_linewidth"], color=color_map[cat])
                fy = kde1d(yc, yi, bw=params["marginal_bw"])
                if fy is not None:
                    ax_right.fill_betweenx(yi, 0, fy, alpha=params["marginal_fill_alpha"], color=color_map[cat])
                    ax_right.plot(fy, yi, linewidth=params["marginal_linewidth"], color=color_map[cat])

            legend_handles.append(Patch(facecolor=color_map[cat] if params["filled"] else "none",
                                        edgecolor=color_map[cat], label=str(cat)))

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
    
    # Etichette dei quadranti
    for lbl in params["labels"].values():
        ax.text(lbl["pos"][0], lbl["pos"][1], lbl["text"],
                ha="center", va="center", **params["labels_style"])

    # Pulizia marginali (se presenti)
    if show_marginals:
        ax_top.set_xlim(params["xlim"]); ax_top.axis("off")
        ax_right.set_ylim(params["ylim"]); ax_right.axis("off")

    fig.tight_layout()
    plt.show()
    return fig, ax