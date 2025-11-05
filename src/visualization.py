import matplotlib.pyplot as plt
import numpy as np
from graphviz import Digraph

def _add_nodes_edges(node, dot):
    if node.char is not None:
        # Leaf node
        label = f"'{node.char}'\\n({node.freq})"
        dot.node(str(id(node)), label)
    else:
        # Internal node
        label = str(node.freq)
        dot.node(str(id(node)), label)
        if node.left:
            dot.edge(str(id(node)), str(id(node.left)), label='0')
            _add_nodes_edges(node.left, dot)
        if node.right:
            dot.edge(str(id(node)), str(id(node.right)), label='1')
            _add_nodes_edges(node.right, dot)

def plot_huffman_tree(tree_root, filename="huffman_tree"):
    """
    Saves the Huffman tree plot to a file.
    """
    dot = Digraph()
    dot.attr('node', shape='circle')
    _add_nodes_edges(tree_root, dot)
    dot.render(filename, view=False, format='png')
    print(f"Huffman tree plot saved to {filename}.png")


def plot_llr_histogram(llrs, title="LLR Histogram"):
    """
    Plots the histogram of LLRs.
    """
    plt.figure(figsize=(10, 6))
    plt.hist(llrs, bins=50, density=True, alpha=0.75, label='LLR Distribution')
    plt.title(title)
    plt.xlabel("LLR Value")
    plt.ylabel("Probability Density")
    plt.grid(True)
    plt.legend()

    filename = title.replace(" ", "_").lower() + ".png"
    plt.savefig(filename)
    print(f"LLR histogram saved to {filename}")
    plt.close()

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
