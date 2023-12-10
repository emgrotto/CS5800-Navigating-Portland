import geopandas as gpd
import pandas as pd
from shapely import wkt
import networkx as nx
import contextily as ctx
import matplotlib.pyplot as plt

groc = pd.read_csv('locations data/Portland Bus Route Locations- Grocery Stores.csv')
scho = pd.read_csv('locations data/Portland Bus Route Locations- Schools.csv')
hc = pd.read_csv('locations data/Portland Bus Route Locations- Healthcare Facilities.csv')
all = pd.concat([groc,scho,hc])
all['WKT'] = gpd.GeoSeries.from_wkt(all['WKT'])
all_gdf = gpd.GeoDataFrame(all, geometry = 'WKT').set_crs("EPSG:4326")
all_gdf = all_gdf.to_crs("EPSG:3857")

# plot priority locations data
def gen_plot():
    ax = all_gdf.plot(figsize=(10, 8), column = 'description', categorical=True,legend=True)
    ax.axis('off')
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=15, crs=all_gdf.crs)
    plt.suptitle('Portland Priority Locations', fontsize=10) 
    plt.savefig('figs/priority_locations.png')

#gen_plot()

### graph code from 'load_graph.py'
intersections = gpd.read_file('data/intersections.geojson')
# set geometry to the geometry column
intersections = intersections.set_geometry('geometry')


roads = gpd.read_file('data/portland_roads.geojson')
intersections = gpd.read_file('data/intersections.geojson')
# set geometry to the geometry column
intersections = intersections.set_geometry('geometry')

def load_graph(roads):
    G = nx.Graph()
    # populate edges as roads with their length as weight
    for i in range(len(roads)):
        # get coordinates of road
        road = roads.iloc[i]
        length = road["Shape_Length"]
        # add road as edge to graph, having its start and end coordinates as the intersection nodes
        first_coord = road["geometry"].coords[0]
        last_coord = road["geometry"].coords[-1]
        # only add if its not a road to itself
        if first_coord != last_coord:
            # casting to int to approximate coordinates as nodes
            G.add_edge((int(first_coord[0]), int(first_coord[1])), (int(last_coord[0]), int(last_coord[1])), weight=length)
            
    return G

G = load_graph(roads)


# loop intersections and all_gdf and add columns for distance from each node to points of interest
# store distance
for i in range(len(all_gdf)):
    point = all_gdf.iloc[i,0]
    intersections[all_gdf.iloc[i,1]] = intersections['geometry'].distance(point)

# extact minimum distances and create list of priority nodes
loc_list = []
for i in range(4,36):
    min_node = intersections.iloc[:,i].idxmin()
    tup = (intersections.iloc[min_node].geometry.x ,intersections.iloc[min_node].geometry.y)
    loc_list.append(tup)

# using simple path does not exectute d/t running time
shortest_paths = nx.shortest_path(G, source = loc_list[0], weight='weight')
shortest_path_cost = nx.shortest_path_length(G, source = loc_list[0], weight='weight')

for node in loc_list:
    path = shortest_paths[node]
    if set(loc_list).issubset(path):
        print (shortest_paths[node])
        
    
'''def find_shortest_path(p):
    for path in p:
        
        if set(loc_list).issubset(path):
            print(path)
            return(path)
        
       #if all(x in path for x in loc_list):
           # print(path)
          #  return path

find_shortest_path(shortest_paths)'''