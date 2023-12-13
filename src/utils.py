import networkx as nx
import pandas as pd
import geopandas as gpd

def read_data():
    """
    Returns a geodataframe of all the priority locations, a geodataframe of all the intersections, and a geodataframe of all the roads
    """
    groc = pd.read_csv('data/Portland Bus Route Locations- Grocery Stores.csv')
    scho = pd.read_csv('data/Portland Bus Route Locations- Schools.csv')
    hc = pd.read_csv('data/Portland Bus Route Locations- Healthcare Facilities.csv')
    all = pd.concat([groc,scho,hc])
    all['WKT'] = gpd.GeoSeries.from_wkt(all['WKT'])
    all_gdf = gpd.GeoDataFrame(all, geometry = 'WKT').set_crs("EPSG:4326")
    all_gdf = all_gdf.to_crs("EPSG:3857")

    intersections = gpd.read_file('data/intersections.geojson')
    # set geometry to the geometry column
    intersections = intersections.set_geometry('geometry')

    roads = gpd.read_file('data/portland_roads.geojson')
    
    return all_gdf, intersections, roads

def load_graph(roads):
    """
    Returns a graph of the roads
    """
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

def get_largest_component_as_graph(G):
    """
    Returns the largest connected component of the graph
    """
    # get largest connected component
    largest_component = max(nx.connected_components(G), key=len)
    # create subgraph of largest connected component
    G = G.subgraph(largest_component)
    return G

