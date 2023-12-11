import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import networkx as nx
import contextily as ctx
import matplotlib.pyplot as plt
from utils import load_graph, read_data

# import data
all_gdf, intersections, roads = read_data()

# plot priority locations data
def gen_plot():
    ax = all_gdf.plot(figsize=(10, 8), column = 'description', categorical=True,legend=True)
    ax.axis('off')
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=15, crs=all_gdf.crs)
    plt.suptitle('Portland Priority Locations', fontsize=10) 
    plt.savefig('figs/priority_locations.png')

#gen_plot()

G = load_graph(roads)

# loop intersections and all_gdf and add columns for distance from each node to points of interest
# store distance
for i in range(len(all_gdf)):
    point = all_gdf.iloc[i,0]
    intersections[all_gdf.iloc[i,1]] = intersections['geometry'].distance(point)

print(intersections.head())

# extract minimum distances and create list of priority nodes
loc_list = []
for i in range(4,36):
    min_node = intersections.iloc[:,i].idxmin()
    tup = (intersections.iloc[min_node].geometry.x ,intersections.iloc[min_node].geometry.y)
    loc_list.append(tup)

print(len(loc_list))
print(loc_list[0])

# using simple path does not exectute d/t running time
shortest_paths = nx.shortest_path(G, source = loc_list[0], weight='weight')
shortest_path_cost = nx.shortest_path_length(G, source = loc_list[0], weight='weight')

print(f"Shortest path from {loc_list[0]} to {loc_list[1]}:")
print(shortest_paths[loc_list[1]])
print(shortest_path_cost[loc_list[1]])

for node in loc_list:
    path = shortest_paths[node]
    if set(loc_list).issubset(path):
        print (shortest_paths[node])
        
    
# find the shortest path between the two points
tsp = nx.approximation.traveling_salesman_problem
path = tsp(G, nodes=loc_list, cycle=False)
sub_graph = G.subgraph(path)
locations = {loc: (Point(loc).x, Point(loc).y) for loc in path}

fig, ax = plt.subplots(figsize=(50, 50))
nx.draw(
    sub_graph,
    locations,
    ax = ax,
    node_size=40,
    width=8,
    node_color="k",
    edge_color="k",
    alpha=0.8,
)
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=15, crs=intersections.crs)
plt.savefig(f'figs/shortest_path.png', bbox_inches='tight')
