import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation, PillowWriter

# Initialize a smaller directed graph
G = nx.DiGraph()
edges = [
    (1, 2), (2, 3), (3, 4), (4, 1), 
    (2, 4), (4, 5), (5, 1), (3, 5)
]
G.add_edges_from(edges)

# PageRank setup with initial ranks
iterations = 10  # Reduced number of PageRank iterations to animate
initial_ranks = {node: 1.0 for node in G.nodes()}  # Start all nodes with rank 1.0
ranks_history = [initial_ranks.copy()]

# PageRank computation with history tracking for visualization
for i in range(iterations):
    ranks = nx.pagerank(G, alpha=0.85, personalization=ranks_history[-1])
    ranks_history.append(ranks)

# Set up positions and initial plot
pos = nx.spring_layout(G, seed=42)  # Fixed layout for consistent display
fig, ax = plt.subplots(figsize=(8, 6))

# Custom color map setup
cmap = plt.cm.get_cmap("cool")  # Choose 'cool' colormap for different color range

# Animation update function
def update(num):
    ax.clear()
    
    # Get the ranks for the current iteration
    current_ranks = ranks_history[num]
    max_rank = max(current_ranks.values())
    
    # Adjust node color and size based on rank using custom color map
    color_map = [
        cmap(current_ranks[node] / max_rank) for node in G.nodes()
    ]
    node_sizes = [2000 * current_ranks[node] for node in G.nodes()]

    # Draw the directed graph with updated ranks
    nx.draw(G, pos, with_labels=True, node_color=color_map, node_size=node_sizes, edge_color="gray", ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrowstyle="->", arrowsize=15, ax=ax)

    # Update title to show current iteration
    ax.set_title(f"PageRank Iteration {num + 1}")

# Create the animation
ani = FuncAnimation(fig, update, frames=iterations + 1, interval=700, repeat=False)

plt.show()

# Optional: Save as a GIF
ani.save("pagerank_small_graph_colored_animation.gif", writer=PillowWriter(fps=2))