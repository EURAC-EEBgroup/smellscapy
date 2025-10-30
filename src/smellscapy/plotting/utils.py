""" funzioni diverse """
from matplotlib.ticker import MultipleLocator
import numpy as np
from scipy.stats import gaussian_kde
import matplotlib as mpl
import matplotlib.pyplot as plt



def get_default_plot_params():
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
        "contour_color": "blue",
        "contour_width": 1.0,
        "fill_color": "blue",
        "fill_alpha": 0.4,

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
        "hdr_p": 0.5,

        # Scatter
        "show_points": True,
        "point_size": 30,
        "point_alpha": 0.2,
        "point_color": "blue",

        # Raggruppamento/colori
        "group_by_col": None,
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
        "marginal_fill_alpha": 0.05,
        "marginal_bw": None,           # banda KDE 1D

        "savefig": True,
        "dpi": 300,
    }

    return params


def update_params(params, **kwargs):
    """
    Update default parameters with ones provided by the user

    Parameters
    ----------
    params : dict, required
        A dictionary with default parameters

    Returns
    -------
    params : dict
        Updated dictionary


    """
    for key, value in kwargs.items():
        if key in params and isinstance(params[key], dict) and isinstance(value, dict):
            params[key].update(value)
        else:
            params[key] = value

    return params



def create_density_figure(params):
    if params["show_marginals"]:
        fig = plt.figure(figsize=params["figsize"])
        gs = fig.add_gridspec(
            nrows=2, ncols=2,
            width_ratios=[4, params["marginal_height_ratio"]],
            height_ratios=[params["marginal_height_ratio"], 4],
            hspace=0.04, wspace=0.04
        )
        ax_top = fig.add_subplot(gs[0, 0])
        ax_top.set_xlim(params["xlim"]); ax_top.axis("off")

        ax = fig.add_subplot(gs[1, 0], sharex=ax_top)

        ax_right = fig.add_subplot(gs[1, 1], sharey=ax)
        ax_right.set_ylim(params["ylim"]); ax_right.axis("off")
    else:
        fig, ax = plt.subplots(figsize=params["figsize"])
        ax_top = None
        ax_right = None

    return fig, ax, ax_top, ax_right



def set_fig_layout(ax, params):
    """
    
    """
    
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
    ax.axhline(0, color=params["axis_line_color"], linestyle=params["axis_line_style"], linewidth=params["axis_line_width"])
    ax.axvline(0, color=params["axis_line_color"], linestyle=params["axis_line_style"], linewidth=params["axis_line_width"])

    x_vals = np.linspace(params["xlim"][0], params["xlim"][1], 200)
    ax.plot(x_vals,  x_vals, linestyle=params["diag_style"], color=params["diag_color"], linewidth=params["diag_width"])
    ax.plot(x_vals, -x_vals, linestyle=params["diag_style"], color=params["diag_color"], linewidth=params["diag_width"])


    # Etichette dei quadranti
    for lbl in params["labels"].values():
        ax.text(lbl["pos"][0], lbl["pos"][1], lbl["text"],
                ha="center", va="center", **params["labels_style"])
        
    return ax



def kde_on_grid(x_sub, y_sub, XX, YY):
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
    cmap = mpl.colormaps.get("tab20")

    return {c: cmap(i % 10) for i, c in enumerate(categories)}



def add_contour_HDR_50(ax, XX, YY, ZZ, params, color=None):
    if ZZ is not None:
        fill_color = color if color else params["fill_color"]
        contour_color = color if color else params["contour_color"]

        thr, zmax = hdr_threshold_from_grid(ZZ, params["hdr_p"], params["xlim"], params["ylim"])
        if thr < zmax:
            ax.contourf(XX, YY, ZZ, levels=[thr, zmax],
                        colors=[fill_color], alpha=params["fill_alpha"])
            ax.contour(XX, YY, ZZ, levels=[thr],
                        colors=[contour_color], linewidths=params["contour_width"])
            
    return ax



# --------- MODIFICA: livelli con esclusione estremi inferiori ----------
def draw_contours(params, ax_, XX, YY, Z, color=None, cmap=None, levels=5, filled=False, lw=1, alpha=1):

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


   


def add_marginals(x, xi, y, yi, ax_top, ax_right, params, color=None):
    fill_color = color if color else params["fill_color"]
    contour_color = color if color else params["contour_color"]

    fx = kde1d(x, xi, bw=params["marginal_bw"])
    if fx is not None:
        ax_top.fill_between(xi, 0, fx, alpha=params["marginal_fill_alpha"], color=fill_color)
        ax_top.plot(xi, fx, linewidth=params["marginal_linewidth"], color=contour_color)
    fy = kde1d(y, yi, bw=params["marginal_bw"])
    if fy is not None:
        ax_right.fill_betweenx(yi, 0, fy, alpha=params["marginal_fill_alpha"], color=fill_color)
        ax_right.plot(fy, yi, linewidth=params["marginal_linewidth"], color=contour_color)

    return ax_top, ax_right



def get_category_order(params):
    if params.get("category_order") is not None:
        order = [c for c in params["category_order"] if c in cats.cat.categories]
        order += [c for c in cats.cat.categories if c not in order]
    else:
        order = sorted(cats.cat.categories)

    cats = cats.cat.reorder_categories(order, ordered=True)

    return order

