import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation, PillowWriter

# Initialize a larger graph with more vertices and edges
G = nx.Graph()
edges = [
    (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (2, 5),
    (3, 4), (3, 6), (4, 5), (4, 6), (5, 6), (5, 7),
    (6, 7), (6, 8), (7, 8), (7, 9), (8, 9), (8, 10),
    (9, 10), (1, 10), (3, 8), (2, 7)
]
G.add_edges_from(edges)

# Find triangles in the graph
triangles = [list(triangle) for triangle in nx.enumerate_all_cliques(G) if len(triangle) == 3]

# Set up positions and initial plot
pos = nx.spring_layout(G, seed=42)  # Using a fixed seed for consistent layout
fig, ax = plt.subplots(figsize=(8, 6))
default_color = "lightblue"
triangle_color = "orange"
color_map = [default_color for node in G.nodes()]
nx.draw(G, pos, with_labels=True, node_color=color_map, ax=ax)

# Animation update function
def update(num):
    ax.clear()
    
    # Draw graph with default node colors
    nx.draw(G, pos, with_labels=True, node_color=default_color, ax=ax)
    
    # Highlight the current triangle
    if num < len(triangles):
        current_triangle = triangles[num]
        triangle_edges = [(current_triangle[i], current_triangle[j]) for i in range(3) for j in range(i+1, 3)]
        
        # Highlight nodes in the triangle
        color_map = [
            triangle_color if node in current_triangle else default_color
            for node in G.nodes()
        ]
        nx.draw(G, pos, with_labels=True, node_color=color_map, ax=ax)
        
        # Highlight triangle edges
        nx.draw_networkx_edges(G, pos, edgelist=triangle_edges, edge_color="blue", width=2, ax=ax)
        
        # Update title to show current triangle
        ax.set_title(f"Triangle Step {num+1}: Nodes {current_triangle}")
    else:
        ax.set_title("All triangles highlighted")

# Create the animation
ani = FuncAnimation(fig, update, frames=len(triangles), interval=1000, repeat=False)

plt.show()

# Optional: Save as a GIF
ani.save("triangle_counting_animation.gif", writer=PillowWriter(fps=1))