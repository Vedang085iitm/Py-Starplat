import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation, PillowWriter

# Initialize the graph
G = nx.Graph()
edges = [
    (1, 2), (1, 3), (2, 3), (2, 4),
    (3, 4), (3, 5), (4, 5), (5, 6)
]
G.add_edges_from(edges)

# Use a simple greedy approach to find an approximate vertex cover
# This will give us a list of vertices for the cover in an ordered sequence
vertex_cover = set()
for u, v in edges:
    if u not in vertex_cover and v not in vertex_cover:
        vertex_cover.add(u)

# Prepare the ordered list for animation
vertex_cover_sequence = list(vertex_cover)

# Set up positions and initial plot
pos = nx.spring_layout(G)
fig, ax = plt.subplots(figsize=(8, 6))
default_color = "lightblue"
highlight_color = "orange"
color_map = [default_color for node in G.nodes()]
nx.draw(G, pos, with_labels=True, node_color=color_map, ax=ax)

# Animation update function
def update(num):
    ax.clear()
    
    # Update color map for vertex cover nodes up to the current frame
    current_cover = vertex_cover_sequence[:num+1]
    color_map = [
        highlight_color if node in current_cover else default_color
        for node in G.nodes()
    ]
    
    # Draw graph with updated color map
    nx.draw(G, pos, with_labels=True, node_color=color_map, ax=ax)
    
    # Highlight edges covered by the selected nodes
    covered_edges = [
        edge for edge in G.edges() if edge[0] in current_cover or edge[1] in current_cover
    ]
    nx.draw_networkx_edges(G, pos, edgelist=covered_edges, edge_color="blue", width=2, ax=ax)
    
    # Update title to show progress
    ax.set_title(f"Vertex Cover Step {num+1}: Covering nodes {current_cover}")

# Create the animation
ani = FuncAnimation(fig, update, frames=len(vertex_cover_sequence), interval=1000, repeat=False)

plt.show()

# Optional: Save as a GIF
ani.save("vertex_cover_animation.gif", writer=PillowWriter(fps=1))