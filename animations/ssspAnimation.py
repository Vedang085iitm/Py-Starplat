import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

# Initialize the graph
G = nx.Graph()
edges = [
    (1, 2, 4), (1, 3, 2), (2, 3, 1), (2, 4, 5),
    (3, 4, 8), (3, 5, 10), (4, 5, 2), (5, 6, 3)
]
G.add_weighted_edges_from(edges)

# Shortest path setup
source_node = 1
shortest_paths = nx.single_source_dijkstra_path_length(G, source=source_node)

# Set up positions and initial plot
pos = nx.spring_layout(G)
fig, ax = plt.subplots(figsize=(8, 6))
color_map = ["lightblue" if node != source_node else "green" for node in G.nodes()]
nx.draw(G, pos, with_labels=True, node_color=color_map, ax=ax)

# Prepare edges for the animation
shortest_path_edges = []
for target_node in shortest_paths:
    if target_node != source_node:
        path = nx.shortest_path(G, source=source_node, target=target_node, weight='weight')
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        shortest_path_edges.extend(path_edges)

# Animation update function
def update(num):
    ax.clear()
    # Draw all nodes and edges initially
    nx.draw(G, pos, with_labels=True, node_color=color_map, ax=ax)
    
    # Highlight edges step-by-step
    nx.draw_networkx_edges(
        G, pos, edgelist=shortest_path_edges[:num], edge_color="blue", width=2, ax=ax
    )
    # Update title to show current edge
    if num < len(shortest_path_edges):
        ax.set_title(f"Highlighting edge {shortest_path_edges[num]}")
    else:
        ax.set_title("All shortest paths highlighted")

# Create the animation
ani = FuncAnimation(fig, update, frames=len(shortest_path_edges)+1, interval=500, repeat=False)

plt.show()

# Optional: Save as a GIF
ani.save("sssp_animation.gif", writer=PillowWriter(fps=60))