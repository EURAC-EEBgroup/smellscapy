import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from smellscapy.calculations import calculate_pleasantness, calculate_presence

def plot_joint(df, xlim=(-1, 1), ylim=(-1, 1)):

    plt.figure(figsize=(8, 8))
    x = df['pleasantness_score'].values
    y = df['presence_score'].values

    # Calculate density with KDE
    xy = np.vstack([x, y])
    kde = gaussian_kde(xy)
    z = kde(xy)

    # Calculate 50% density
    z_sorted = np.sort(z)
    cdf = np.cumsum(z_sorted)
    cdf /= cdf[-1]
    z_50 = z_sorted[np.searchsorted(cdf, 0.5)]

    # Contour grid
    xi, yi = np.mgrid[
        xlim[0]:xlim[1]:100j,
        ylim[0]:ylim[1]:100j
    ]
    zi = kde(np.vstack([xi.ravel(), yi.ravel()])).reshape(xi.shape)

    # Contour 50° percentile
    plt.contourf(xi, yi, zi, levels=[z_50, zi.max()], colors=['grey'], alpha=0.6)
    plt.contour(xi, yi, zi, levels=[z_50], colors='black', linewidths=1)

    plt.scatter(x, y, color='grey')    

    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.xlabel('Pleasantness')
    plt.ylabel('Presence')
    plt.axhline(0, color='grey', linestyle='--', linewidth=1)
    plt.axvline(0, color='grey', linestyle='--', linewidth=1)

    # Diagonal lines
    x_vals = np.linspace(xlim[0], xlim[1], 200)
    plt.plot(x_vals, x_vals, linestyle='--', color='black', linewidth=0.8)
    plt.plot(x_vals, -x_vals, linestyle='--', color='black', linewidth=0.8)

    # Diagonal lines text
    plt.text(-0.6, 0.5, 'Overpowering', ha='left', va='bottom', fontsize=10)
    plt.text(-0.6, -0.5, 'Detached', ha='left', va='top', fontsize=10)
    plt.text(0.4, 0.5, 'Engaging', ha='left', va='bottom', fontsize=10)
    plt.text(0.4, -0.5, 'Light', ha='left', va='top', fontsize=10)


    plt.minorticks_on()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()

    plt.savefig("50percentile_plot.png", dpi=300, bbox_inches='tight')
    plt.show()   