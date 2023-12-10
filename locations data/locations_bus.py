import geopandas as gpd
import pandas as pd
from shapely import wkt
import networkx as nx


groc = pd.read_csv('locations data/Portland Bus Route Locations- Grocery Stores.csv')
scho = pd.read_csv('locations data/Portland Bus Route Locations- Schools.csv')
hc = pd.read_csv('locations data/Portland Bus Route Locations- Healthcare Facilities.csv')
all = pd.concat([groc,scho,hc])
all['WKT'] = gpd.GeoSeries.from_wkt(all['WKT']).set_crs("EPSG:3857")
all_gdf = gpd.GeoDataFrame(all, geometry = 'WKT')


### graph code form 'load_graph.py'
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

for i in range(len(all_gdf)):
    point = all_gdf.iloc[i,0]
    intersections[all_gdf.iloc[i,1]] = intersections['geometry'].distance(point)


### NEED TO GET NODE NAME OUT OF INTERSECTIONS GDF###
# idea for path filter
'''path_nodes = lambda x: 'node info here' in x and 'more node info' in x 

shortest_paths = nx.all_shortest_paths(G,weight="weight")
filter(path_nodes,shortest_paths)'''