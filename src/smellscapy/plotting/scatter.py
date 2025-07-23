import numpy as np
import matplotlib as plt
from smellscapy.calculations import calculate_pleasantness, calculate_presence

def plot_scatter(df, xlim=(-1, 1), ylim=(-1, 1)):

    plt.figure(figsize=(8, 8))
    x = df['pleasantness_score'].values
    y = df['presence_score'].values

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

    plt.savefig("scatter_plot.png", dpi=300, bbox_inches='tight')
    plt.show()   