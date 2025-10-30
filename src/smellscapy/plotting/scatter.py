import numpy as np
import matplotlib.pyplot as plt
from smellscapy.plotting.utils import update_params, set_fig_layout, get_default_plot_params


def plot_scatter(df, **kwargs):

    # Default values dictianary
    params = get_default_plot_params()
    params['filename'] = "scatter_plot.png"
    params = update_params(params, **kwargs)

    # ----------------- Figura/Axes -----------------
    fig = plt.figure(figsize=params["figsize"])
    ax = fig.gca()

    ax = set_fig_layout(ax, params)

    if params["group_by_col"] is not None and params["group_by_col"] in df.columns:
        ax.legend(title=params["group_by_col"])
        df_subgroups = df.groupby(params["group_by_col"])
        for name, subgroup in df_subgroups:
            x = subgroup['pleasantness_score']
            y = subgroup['presence_score']
            ax.scatter(x, y, s=params["point_size"], label=str(name), alpha=0.8)
    else:
        # Calculate coordinates
        x = df['pleasantness_score'].values
        y = df['presence_score'].values
        ax.scatter(x, y, color=params["point_color"], s=params["point_size"], alpha=0.8)


    # Saving
    if params["savefig"]:
        plt.savefig(params["filename"], dpi=params["dpi"], bbox_inches='tight')

    fig.tight_layout()
    plt.show()
    return fig, ax