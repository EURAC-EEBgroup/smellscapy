import numpy as np
import matplotlib.pyplot as plt
from smellscapy.plotting.utils import update_params, set_fig_layout, get_default_plot_params


def plot_scatter(df, **kwargs):
    """
    Generates a scatter plot showing the relationship two key variables in the provided survey DataFrame: `pleasantness_score` (X-axis), and `presence_score` (Y-axis)

    This function allows users to customise plot parameters though `**kwargs`

    Parameters
    ----------
    df : pd.DataFrame
        A DataFrame containing survey data. It must include at least the columns  
        `'pleasantness_score'` and `'presence_score'`.

    **kwargs : dict, optional** 
        Additional keyword arguments to override default plotting parameters, including:  
        - `figsize` : tuple, size of the figure in inches.  
        - `point_color` : str, colour of scatter points.  
        - `point_size` : int or float, size of each marker.  
        - `group_by_col` : str, column name used for grouping and colouring subsets.  
        - `savefig` : bool, whether to save the plot to file.  
        - `filename` : str, output file name.  
        - `dpi` : int, figure resolution for saved image.

    Returns
    -------
    fig : matplotlib.figure.Figure  
        The Matplotlib figure object of the generated plot.

    ax : matplotlib.axes.Axes  
        The corresponding axes object containing the scatter plot.

    Examples
    --------
        >>> import pandas as pd
        >>> from smellscapy.databases.DataExample import load_example_data
        >>> from smellscapy.surveys import validate
        >>> from smellscapy.calculations import calculate_presence, calculate_pleasantness
        >>> from smellscapy.plotting import plot_scatter
        >>> df = load_example_data()
        >>> df, excl_df = validate(df)
        >>> df = calculate_presence(df)
        >>> df = calculate_pleasantness(df)
        >>> fig, ax = plot_scatter(df, point_color="steelblue", point_size=50)
    
    """

    # Params
    params = get_default_plot_params()     
    params['filename'] = "scatter_plot.png"
    params = update_params(params, **kwargs)

    #Figure layout
    fig = plt.figure(figsize=params["figsize"])
    ax = fig.gca()
    ax = set_fig_layout(ax, params)

    #Scatter with optional grouping
    if params["group_by_col"] is not None and params["group_by_col"] in df.columns:
        ax.legend(title=params["group_by_col"])
        df_subgroups = df.groupby(params["group_by_col"])
        for name, subgroup in df_subgroups:
            x = subgroup['pleasantness_score']
            y = subgroup['presence_score']
            ax.scatter(x, y, s=params["point_size"], label=str(name), alpha=0.8)
    else:
        x = df['pleasantness_score'].values
        y = df['presence_score'].values
        ax.scatter(x, y, color=params["point_color"], s=params["point_size"], alpha=0.8)
    
    # Saving
    if params["savefig"]:
        plt.savefig(params["filename"], dpi=params["dpi"], bbox_inches='tight')

    fig.tight_layout()
    plt.show()
    return fig, ax