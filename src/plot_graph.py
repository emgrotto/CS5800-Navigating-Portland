import networkx as nx
import matplotlib.pyplot as plt
import contextily as ctx
from shapely.geometry import Point
from utils import load_graph, read_data

# import data
all_gdf, intersections, roads = read_data()

print("Number of roads: ", len(roads))
print("Number of intersections: ", len(intersections))

G = load_graph(roads)

# validate graph
print("Graph information:")
print("Number of nodes: ", G.number_of_nodes())
print("Number of edges: ", G.number_of_edges())
print("Number of connected components: ", nx.number_connected_components(G))
degrees = [val for (node, val) in G.degree()]
print("max degree: ", max(degrees))
print("min degree: ", min(degrees))

for i in range(1, 9):
    print(f"Number of nodes with degree {i}: ", len([val for (node, val) in G.degree() if val == i]))

# get coordinate positions from the nodes so that we can plot it against a basemap.
nodes = list(G.nodes)
positions = {node: (Point(node).x, Point(node).y) for node in nodes}

# create a figure and axis
fig, ax = plt.subplots(figsize=(100, 100))

# get all connected components
C = list((G.subgraph(c) for c in nx.connected_components(G)))
colors = ["darkblue", "lightseagreen", "lightcoral", "fuchsia", "darkviolet", "indigo", "mediumblue", "purple"]
ci = 0

# iterate through connected components and plot each one a different color
for g in C:
    print(f"Number of nodes in connected component: {g.number_of_nodes()}")
    # pick a random color for each connected component
    hexadecimal_alphabets = '0123456789ABCDEF'
    c = [colors[ci]] * g.number_of_nodes()
    nx.draw(g, 
            positions, 
            ax=ax, 
            node_size=10, 
            width=5,
            node_color=c, 
            edge_color=c, 
            vmin=0.0, 
            vmax=1.0, 
            alpha=0.8, 
            with_labels=False
            )
    ci += 1

"""
large_component = max(nx.connected_components(G), key=len)

print("Graph information for the largest connected component:")
print("Number of nodes: ", largest_component.number_of_nodes())
print("Number of edges: ", largest_component.number_of_edges())
print("max degree: ", max([val for (node, val) in largest_component.degree()]))
print("min degree: ", min([val for (node, val) in largest_component.degree()]))

nx.draw(
    largest_component,
    positions,
    ax=ax,
    node_size=2,
    node_color="k",
    edge_color="k",
    alpha=0.8,
)
"""

ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=15, crs=intersections.crs)
plt.savefig(f'figs/connected_components.png', bbox_inches='tight')
