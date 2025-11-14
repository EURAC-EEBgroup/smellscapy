""" funzioni diverse """
from matplotlib.ticker import MultipleLocator
import numpy as np
from scipy.stats import gaussian_kde
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd



def get_default_plot_params():
    """
    Return the default configuration dictionary for plots.

    The returned dictionary contains default values for axis limits, labels,
    figure size, 2D KDE contour settings, scatter plot appearance, grouping
    and colour handling, quadrant labels, marginal distributions, and
    saving options.

    Parameters
    ----------
    xlim : tuple(float, float)
        Default x-axis limits (pleasantness), initialised to (-1, 1).
    ylim : tuple(float, float)
        Default y-axis limits (presence), initialised to (-1, 1).
    figsize : tuple(float, float)
        Figure size in inches, default (8, 8).
    xlabel : str
        Label for the x-axis, default "Pleasantness".
    ylabel : str
        Label for the y-axis, default "Presence".
    levels : int or array-like
        Number of contour bands or explicit boundary levels. By default,
        10 levels are used.
    filled : bool
        If True, use filled contours (e.g. `contourf`); otherwise, only
        contour lines.
    extend : {"neither", "min", "max", "both"}
        Argument passed to Matplotlib for handling out-of-range values in
        filled contours.
    contour_linewidth : float
        Line width used for contour lines (legacy / backup parameter).
    contour_color : str
        Default colour for contour lines.
    contour_width : float
        Line width for HDR or contour outlines.
    fill_color : str
        Default fill colour for filled areas.
    fill_alpha : float
        Opacity for filled regions (0–1).
    skip_low_levels : int
        Number of lowest-density bands to drop (0 means keep all).
    min_frac : float or None
        If set to a value in [0, 1], discard all contour levels below
        `min_frac * Z.max()`.
    axis_line_color : str
        Colour of the central horizontal and vertical axes (x=0, y=0).
    axis_line_style : str
        Line style for central axes.
    axis_line_width : float
        Line width for central axes.
    diag_color : str
        Colour of the ±45° diagonals.
    diag_style : str
        Line style for diagonals.
    diag_width : float
        Line width for diagonals.
    xmajor_step, xminor_step : float
        Spacing for major and minor ticks on the x-axis.
    ymajor_step, yminor_step : float
        Spacing for major and minor ticks on the y-axis.
    grid_major : dict
        Style dictionary for major grid lines (linestyle, linewidth, alpha).
    grid_minor : dict
        Style dictionary for minor grid lines.
    minor_tick_length : float
        Length of minor tick marks; default 0 (invisible).
    eval_n : int
        Number of evaluation points per axis for the 2D KDE grid.
    hdr_p : float
        Probability mass of the high-density region (HDR), default 0.5.
    show_points : bool
        Whether to overlay individual data points.
    point_size : float
        Marker size for scatter points.
    point_alpha : float
        Transparency for scatter points.
    point_color : str or tuple
        Default colour for scatter points.
    group_by_col : str or None
        Name of the column used for categorical grouping.
    palette : dict, list, tuple or str
        Palette specification used by `build_categorical_palette`.
    legend_loc : str
        Legend location string (passed to Matplotlib).
    category_order : list or None
        Optional ordering of categories for plotting and legends.
    show_quadrant_labels : bool
        Whether to show textual labels in the four quadrants.
    labels : dict
        Mapping of label identifiers to positions and text
        (e.g. "Overpowering", "Detached", etc.).
    labels_style : dict
        Text style for quadrant labels (fontsize, fontstyle, alpha, ...).
    show_marginals : bool
        Whether to create axes and draw 1D KDE marginals.
    marginal_height_ratio : float
        Relative size of top and right marginal axes w.r.t. main axes.
    marginal_linewidth : float
        Line width of marginal KDE curves.
    marginal_fill_alpha : float
        Opacity of 1D KDE filled regions.
    marginal_bw : float or None
        Bandwidth for 1D KDE; if None, GaussianKDE defaults are used.
    savefig : bool
        Flag indicating whether saving is expected downstream.
    dpi : int
        Default resolution in dots per inch for saved figures.

    Returns
    -------
    params : dict
        Dictionary containing all default plotting parameters.

    """

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

        "time_col": None

    }

    return params

def get_default_dynamic_plot_params():
    params = {
        "group_by_col": None,
        "frame_order": None,
        "eval_n": 120,
        "xlim": (-1.0, 1.0),
        "ylim": (-1.0, 1.0),
        "point_size": 6,
        "point_alpha": 0.6,
        "palette": None,
        "write_html": None,
        "show": True,
        "auto_open": False,
        "show_quadrant_labels": True,
        "labels": {
            "overpowering": {"pos": (-0.5,  0.5), "text": "Overpowering"},
            "detached":     {"pos": (-0.5, -0.5), "text": "Detached"},
            "engaging":     {"pos": ( 0.5,  0.5), "text": "Engaging"},
            "light":        {"pos": ( 0.5, -0.5), "text": "Light"},
        },
        "labels_style": {"fontsize": 10, "fontstyle": "italic", "alpha": 0.7},
    }
    return params


def update_params(params, **kwargs):
    """
    Update default parameters with ones provided by the user

    Parameters
    ----------
    params : dict, required
        A dictionary with default parameters
    **kwargs
        Key-value pairs used to update `params`. For each (key, value):
        - If `key` is not present in `params`, it is added.
        - If `key` is present and both `params[key]` and `value` are `dict`,
          then `params[key].update(value)` is performed.
        - Otherwise, `params[key]` is replaced by `value`.

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
    """
    Create a Matplotlib figure and axes layout for 2D density plots, with
    optional marginal axes.

    If `params["show_marginals"]` is True, the function creates a 2x2
    GridSpec layout with:
      - top-left: x-axis marginal KDE (`ax_top`)
      - bottom-left: main density plot (`ax`)
      - bottom-right: y-axis marginal KDE (`ax_right`)

    The size of the marginal axes relative to the main axes is controlled by
    `params["marginal_height_ratio"]`. If `show_marginals` is False, only a
    single main axes is created.

    Parameters
    ----------
    params : dict
        Plot configuration dictionary, typically from `get_default_plot_params()`.
        The following keys are used:
        - "show_marginals" : bool
        - "figsize" : tuple(float, float)
        - "xlim", "ylim" : axis limits
        - "marginal_height_ratio" : float

    Returns
    -------
    fig : matplotlib.figure.Figure
        The created Figure.
    ax : matplotlib.axes.Axes
        The main axes for the 2D density plot.
    ax_top : matplotlib.axes.Axes or None
        Axes for the x-direction marginal KDE, or None if `show_marginals`
        is False.
    ax_right : matplotlib.axes.Axes or None
        Axes for the y-direction marginal KDE, or None if `show_marginals`
        is False.
    """

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
    Configure axes layout, grid, central axes, diagonals and quadrant labels.

    This function applies a consistent visual style to the main 2D pleasantness–
    presence axes, including axis limits and labels, tick locators, grid styles,
    central axes at x=0 and y=0, diagonal reference lines, and optional
    quadrant labels.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes object to configure.
    params : dict
        Plot configuration dictionary. The following keys are used:

        - "xlim", "ylim"
        - "xlabel", "ylabel"
        - "xmajor_step", "xminor_step", "ymajor_step", "yminor_step"
        - "grid_major", "grid_minor"
        - "minor_tick_length"
        - "axis_line_color", "axis_line_style", "axis_line_width"
        - "diag_color", "diag_style", "diag_width"
        - "show_quadrant_labels"
        - "labels" (dict with "pos" and "text")
        - "labels_style"

    Returns
    -------
    ax : matplotlib.axes.Axes
        The same axes object, configured.
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
    """
    Compute a 2D Gaussian kernel density estimate (KDE) on a predefined grid.

    Parameters
    ----------
    x_sub : array-like
        1D array of x values.
    y_sub : array-like
        1D array of y values. Must have the same length as `x_sub`.
    XX : ndarray
        2D array of x-coordinates defining the evaluation grid (e.g. from
        `np.meshgrid`).
    YY : ndarray
        2D array of y-coordinates defining the evaluation grid.

    Returns
    -------
    ZZ : ndarray or None
        2D array of KDE values evaluated on (XX, YY) and reshaped to
        `YY.shape`, or None if fewer than 3 valid samples are provided.
    """
    if len(x_sub) < 3:
        return None
    kde = gaussian_kde(np.vstack([x_sub, y_sub]))
    ZZ = kde(np.vstack([XX.ravel(), YY.ravel()])).reshape(YY.shape)

    return ZZ



def hdr_threshold_from_grid(zi, p, xlim, ylim):
    """
    Compute the density threshold for a high-density region (HDR) of mass `p`
    from a 2D KDE grid.

    The function assumes that `zi` has been evaluated on a regular rectangular
    grid spanning `[xlim[0], xlim[1]] × [ylim[0], ylim[1]]`. It computes the
    cell area, sorts the density values in descending order and finds the
    threshold such that the cumulative integral reaches `p` times the total
    mass.

    Parameters
    ----------
    zi : ndarray, shape (ny, nx)
        2D array of density values on a regular grid.
    p : float
        Target probability mass of the HDR (0 < p ≤ 1).
    xlim : tuple(float, float)
        x-axis limits of the grid.
    ylim : tuple(float, float)
        y-axis limits of the grid.

    Returns
    -------
    threshold : float
        Density value defining the HDR boundary, i.e. the smallest
        value such that the region {z >= threshold} contains mass `p`.
    zmax : float
        Maximum density value in `zi`.
    """
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
    """
    Compute a 1D Gaussian kernel density estimate (KDE) on a given grid.

    Parameters
    ----------
    values : array-like
        Input sample values. Non-finite values are filtered out before
        computing the KDE.
    grid : array-like
        Points at which to evaluate the 1D KDE.
    bw : float or str or callable, optional
        Bandwidth specification passed to `scipy.stats.gaussian_kde`
        via the `bw_method` argument. If None, the default method of
        `gaussian_kde` is used.

    Returns
    -------
    density : ndarray or None
        KDE evaluated on `grid`, or None if fewer than 3 finite
        samples are available.
    """
    vals = np.asarray(values)
    vals = vals[np.isfinite(vals)]
    if vals.size < 3:
        return None
    kde = gaussian_kde(vals, bw_method=bw)

    return kde(grid)


def build_categorical_palette(categories, palette_param):
    """
    Build a mapping from categories to colours for grouped plots.

    The palette can be specified in several ways:

    - dict: direct mapping `{category: color}`. Missing categories
      default to `"grey"`.
    - str: name of a Matplotlib colormap. Colours are sampled uniformly
      along the colormap range.
    - list/tuple: sequence of colour specifications. If there are fewer
      colours than categories, the list is repeated cyclically.
    - None or unsupported type: fall back to the "tab20" colormap.

    Parameters
    ----------
    categories : iterable
        Sequence of category labels.
    palette_param : dict, list, tuple or str
        Palette specification as described above.

    Returns
    -------
    color_map : dict
        Dictionary mapping each category in `categories` to a colour
        usable in Matplotlib.
    """
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
    """
    Draw the 50% high-density region (HDR) contour on a 2D KDE grid.

    This function computes the HDR threshold using `hdr_threshold_from_grid`
    with probability mass `params["hdr_p"]` (typically 0.5), and plots:

    - a filled region between the HDR threshold and the maximum density
    - an outline contour at the HDR threshold

    Colours for the filled and contour regions can be overridden via the
    `color` argument; otherwise, `params["fill_color"]` and
    `params["contour_color"]` are used.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes on which to draw the HDR region.
    XX, YY : ndarray
        2D arrays defining the evaluation grid (as returned by `np.meshgrid`).
    ZZ : ndarray or None
        2D KDE values on the grid. If None, nothing is drawn.
    params : dict
        Plot configuration dictionary. The following keys are used:
        - "hdr_p", "xlim", "ylim"
        - "fill_color", "fill_alpha"
        - "contour_color", "contour_width"
    color : str or tuple, optional
        Override colour for both filling and outline. If None, defaults
        from `params` are used.

    Returns
    -------
    ax : matplotlib.axes.Axes
        The same axes, with HDR region drawn (if applicable).
    """
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



def draw_contours(params, ax_, XX, YY, Z, color=None, cmap=None, levels=5, filled=False, lw=1, alpha=1):
    """
    Draw 2D KDE contour lines and/or filled bands, with optional exclusion
    of low-density regions.

    The function supports two modes for `levels`:
    - integer: number of density bands; levels are computed automatically
      between `Z.min()` and `Z.max()`, applying `skip_low_levels` or
      `min_frac` from `params`.
    - array-like: explicit sequence of boundary levels, possibly filtered
      by `min_frac` or `skip_low_levels`.

    When `filled=True`, contour bands are drawn with `contourf`, optionally
    using a colormap that fades from transparent to `color`. Contour lines
    can be drawn on top.

    Parameters
    ----------
    params : dict
        Plot configuration dictionary. The following keys are used:
        - "skip_low_levels" : int
        - "min_frac" : float or None
        - "extend" : {"neither", "min", "max", "both"}
    ax_ : matplotlib.axes.Axes
        Axes on which to draw the contours.
    XX, YY : ndarray
        2D arrays defining the evaluation grid.
    Z : ndarray or None
        2D array of density values on the grid. If None, nothing is drawn.
    color : str or tuple, optional
        Base colour for lines and, when `cmap` is None, for filled regions.
    cmap : matplotlib.colors.Colormap or None, optional
        Colormap for filled contours. If None and `filled` is True and
        `color` is provided, a custom colormap fading from transparent white
        to `color` with opacity `alpha` is created.
    levels : int or array-like, optional
        Number of contour bands (if int) or array of boundary levels.
        When `levels` is an int, the default in higher-level functions is
        10 levels.
    filled : bool, optional
        If True, draw filled contours (`contourf`) plus contour lines.
        If False, draw only contour lines.
    lw : float, optional
        Line width for contour lines.
    alpha : float, optional
        Opacity for filled contours (0–1).

    Returns
    -------
    None
        The function modifies `ax_` in place and does not return a value.
    """

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
    """
    Compute and plot 1D KDE marginal distributions along the x and y axes.

    The function uses `kde1d` to estimate the marginals of `x` and `y`
    on the grids `xi` and `yi`, respectively, and draws them on the
    provided marginal axes.

    Parameters
    ----------
    x : array-like
        Sample values for the x variable.
    xi : array-like
        Grid on which to evaluate the x marginal KDE.
    y : array-like
        Sample values for the y variable.
    yi : array-like
        Grid on which to evaluate the y marginal KDE.
    ax_top : matplotlib.axes.Axes
        Axes for the x-direction marginal (top).
    ax_right : matplotlib.axes.Axes
        Axes for the y-direction marginal (right).
    params : dict
        Plot configuration dictionary. The following keys are used:
        - "marginal_bw"
        - "marginal_fill_alpha"
        - "marginal_linewidth"
        - "fill_color"
        - "contour_color"
    color : str or tuple, optional
        Override colour for both filled area and line. If None, values
        from `params["fill_color"]` and `params["contour_color"]` are used.

    Returns
    -------
    ax_top : matplotlib.axes.Axes
        The x marginal axes, updated with the marginal plot.
    ax_right : matplotlib.axes.Axes
        The y marginal axes, updated with the marginal plot.
    """
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
    """
    Determine the plotting order for categorical groups.

    This helper is intended to build an ordered list of categories based on
    a preferred order in `params["category_order"]`, falling back to the
    natural (sorted) order of the underlying categorical variable.

    Notes
    -----
    The implementation assumes the existence of a categorical Series
    `cats` in the enclosing scope, with categories `cats.cat.categories`.
    It then:

    1. If `params["category_order"]` is not None, filters it to keep only
       categories present in `cats.cat.categories` and keeps that order.
    2. Appends any remaining categories from `cats.cat.categories` that
       are not already in the filtered list.
    3. Reorders `cats` using `cats.cat.reorder_categories(order, ordered=True)`.

    Parameters
    ----------
    params : dict
        Plot configuration dictionary. The following key is used:
        - "category_order" : list or None

    Returns
    -------
    order : list
        Final list of category labels in plotting order.
    """
    if params.get("category_order") is not None:
        order = [c for c in params["category_order"] if c in cats.cat.categories]
        order += [c for c in cats.cat.categories if c not in order]
    else:
        order = sorted(cats.cat.categories)

    cats = cats.cat.reorder_categories(order, ordered=True)

    return order


def order_values_for_frames(s: pd.Series, order_override=None):
    """
    Restituisce l'ordine dei valori da usare per gli slider dei frame.
    
    Comportamento:
    - Se l'utente fornisce un ordine esplicito tramite `order_override`,
      quello viene usato (dopo filtraggio dei valori presenti).
    - Se la serie è datetime → ordine cronologico crescente.
    - Altrimenti → ordine di prima apparizione nella serie.
    """
    
    # Se l'utente fornisce un ordine esplicito nei kwargs
    if order_override is not None:
        # Prendi i valori unici nella serie
        unique_vals = list(pd.Series(s.dropna().unique()))

        # Mantieni solo quelli presenti sia nella serie che nell'ordine utente
        ordered = [v for v in order_override if v in unique_vals]

        # Aggiungi eventuali valori presenti nella serie ma mancanti nell'override
        missing = [v for v in unique_vals if v not in ordered]

        return ordered + missing
    
    # Caso datetime → ordina crescente
    if pd.api.types.is_datetime64_any_dtype(s):
        return list(pd.Series(s.dropna().unique()).sort_values())
    
    # Caso generico → ordine di apparizione
    seen = []
    for v in s:
        if pd.notna(v) and v not in seen:
            seen.append(v)
    return seen



def _hdr_level(z: np.ndarray, p: float = 0.5) -> float:
    """
    Return density threshold 't' such that the integral over {z >= t} ≈ p
    of the total mass (discrete approximation).
    """
    if z is None:
        return np.nan

    flat = np.asarray(z, dtype=float).ravel()
    # tieni solo valori finiti
    flat = flat[np.isfinite(flat)]

    if flat.size == 0 or np.all(flat == 0):
        return np.nan

    order = np.argsort(flat)[::-1]
    z_sorted = flat[order]

    cum = np.cumsum(z_sorted)
    total = cum[-1]
    if total == 0 or not np.isfinite(total):
        return np.nan

    cum /= total
    idx = np.searchsorted(cum, p)
    idx = min(idx, z_sorted.size - 1)

    level = z_sorted[idx]
    return float(level)