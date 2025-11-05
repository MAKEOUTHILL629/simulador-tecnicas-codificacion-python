import matplotlib.pyplot as plt
import numpy as np

def plot_constellation(symbols, title="QPSK Constellation"):
    """
    Plots the constellation diagram for a given set of symbols.

    Args:
        symbols (np.ndarray): An array of complex symbols.
        title (str): The title of the plot.
    """
    plt.figure(figsize=(8, 8))
    plt.scatter(np.real(symbols), np.imag(symbols))
    plt.title(title)
    plt.xlabel("In-Phase")
    plt.ylabel("Quadrature")
    plt.grid(True)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.xlim(-1.5, 1.5)
    plt.ylim(-1.5, 1.5)
    plt.gca().set_aspect('equal', adjustable='box')

    # Save the plot to a file instead of showing it
    filename = title.replace(" ", "_").lower() + ".png"
    plt.savefig(filename)
    print(f"Constellation plot saved to {filename}")
    plt.close()
