import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch
import smellscapy.plotting.utils as ut 



def plot_density(df, **kwargs):
    """
    Generates a 2D kernel density estimate (KDE) plot showing the relationship between pleasantness and presence scores in the given dataset. 
    
    Optionally, the function can display individual data points, marginal distributions, and grouped density contours by category.
    By default, the number of contour levels is set to **10**
    This function allows users to customise plot parameters though `**kwargs`

    Parameters
    ----------
    df : pd.DataFrame
        A DataFrame containing survey data. It must include at least the columns  
        `'pleasantness_score'` and `'presence_score'`.

    **kwargs : dict, optional** 
        Additional keyword arguments to override default plotting parameters, including:

        - `eval_n` : int, optional
            Number of evaluation points per axis for the KDE grid.
        - `xlim` : tuple(float, float), optional
            Limits of the x-axis for KDE evaluation and plotting.
        - `ylim` : tuple(float, float), optional
            Limits of the y-axis for KDE evaluation and plotting.
        - `show_points` : bool, optional
            If True, scatter points are drawn on top of the density.
            The default in this function is overridden to ``False``.
        - `point_size` : float, optional
            Marker size for the scattered points.
        - `point_alpha` : float, optional
            Transparency of the scattered points (0-1).
        - `point_color` : str or tuple, optional
            Colour of the scattered points when no grouping is used.
               filled : bool, optional
            If True, filled contours are drawn using a colormap
            (default ``"Grays"`` when not grouped). If False, only
            contour lines are drawn.
        - `levels` : int or sequence, optional
            Number or specific list of contour levels passed to
            ``ut.draw_contours``. **By default, 10 contour levels are drawn.**
        - `contour_linewidth` : float, optional
            Line width for contour lines.
        - `fill_alpha` : float, optional
            Opacity of filled contours (0-1). The default in this
            function is set to ``0.9``.
        - `group_by_col` : str or None, optional
            Name of the column in ``df`` to be used as categorical grouping
            variable. If None or not present in ``df``, a single, global
            density is computed.
        - `category_order` : list, optional
            Explicit order of categories to use when plotting grouped
            densities and building the legend. Categories not listed here
            are appended at the end.
        - `palette` : dict or list, optional
            Categorical palette passed to
            ``ut.build_categorical_palette`` to map each category to a
            specific colour. When grouping is active, each category
            density is drawn with its own colour.
        - `show_marginals` : bool, optional
            If True, 1D KDE marginals are plotted along the top (x) and
            right (y) axes for the global data or for each group.
        - `legend_loc` : str, optional
            Location of the legend when grouping is active (passed to
            ``Axes.legend``).
        - `filename` : str, optional
            Output filename stored in the internal ``params`` dictionary.
            Default is ``"density_plot.png"``. (The current function
            does not save the figure, but this parameter can be used by
            external utilities.)

    Returns
    -------
    fig : matplotlib.figure.Figure  
        The Matplotlib figure object of the generated plot.

    ax : matplotlib.axes.Axes  
        The corresponding axes object containing the scatter plot.

    Examples
    --------
        >>> import pandas as pd
        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> from matplotlib.patches import Patch
        >>> import smellscapy.plotting.utils as ut
        >>> from smellscapy.databases.DataExample import load_example_data
        >>> from smellscapy.surveys import validate
        >>> from smellscapy.calculations import calculate_presence, calculate_pleasantness
        >>> from smellscapy.plotting import plot_scatter
        >>> df = load_example_data()
        >>> df, excl_df = validate(df)
        >>> df = calculate_presence(df)
        >>> df = calculate_pleasantness(df)
        >>> fig, ax = plot_density(df, group_by_col = "Smell_source")
    
    """


    # Params
    params = ut.get_default_plot_params()
    params['filename'] = "density_plot.png"
    params['fill_alpha'] = 0.9
    params['show_points'] = False
    params = ut.update_params(params, **kwargs)

    # Data
    x = np.asarray(df["pleasantness_score"].values)
    y = np.asarray(df["presence_score"].values)

    # Figure
    show_marginals = bool(params["show_marginals"])
    fig, ax, ax_top, ax_right = ut.create_density_figure(params)
    ax = ut.set_fig_layout(ax, params)

    # Helper KDE
    nx = ny = int(params["eval_n"])
    xi = np.linspace(params["xlim"][0], params["xlim"][1], nx)
    yi = np.linspace(params["ylim"][0], params["ylim"][1], ny)
    XX, YY = np.meshgrid(xi, yi, indexing="xy")

    group_by_col = params["group_by_col"]
    category_order = params['category_order']

    # Density
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