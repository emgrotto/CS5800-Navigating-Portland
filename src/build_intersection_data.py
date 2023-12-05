import pandas as pd
import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt
from shapely.geometry import Point

# read in data from geojson and plot with a basemap
gdf = gpd.read_file('data/portland_roads.geojson')

def plot(data, name):
    # plot data with a basemap
    ax = data.plot(aspect=1, figsize=(60, 30), color="k", linewidth=5, markersize=1)
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=15, crs=data.crs)
    plt.suptitle(f'Portland Roads: {name}', fontsize=20)
    plt.savefig(f'figs/{name}.png', bbox_inches='tight')

congress = gdf[gdf['strtname'] == 'CONGRESS ST']
plot(congress, "congress")

def get_intersections(data):
    # build intersection distionary
    # key: tuple of intersection coordinates
    # value: list of indexes of roads that intersect at that intersection
    intersections = {}
    for i in range(len(data)):
        # get coordinates of road
        road = data.iloc[i]
        
        first_coord = road["geometry"].coords[0]
        last_coord = road["geometry"].coords[-1]
        
        first_coord = (int(first_coord[0]), int(first_coord[1]))
        last_coord = (int(last_coord[0]), int(last_coord[1]))

        # add intersection to dictionary
        if (first_coord[0], first_coord[1]) not in intersections:
            intersections[(first_coord[0], first_coord[1])] = {"roads": [road["OBJECTID"]], "neighbors": [(last_coord[0], last_coord[1])]}
        else:
            intersections[(first_coord[0], first_coord[1])]["roads"].append(road["OBJECTID"])
            intersections[(first_coord[0], first_coord[1])]["neighbors"].append((last_coord[0], last_coord[1]))

        if (last_coord[0], last_coord[1]) not in intersections:
            intersections[(last_coord[0], last_coord[1])] = {"roads": [road["OBJECTID"]], "neighbors": [(first_coord[0], first_coord[1])]}
        else:
            intersections[(last_coord[0], last_coord[1])]["roads"].append(road["OBJECTID"])
            intersections[(last_coord[0], last_coord[1])]["neighbors"].append((first_coord[0], first_coord[1]))

    return intersections

def get_dataframe(intersections):
    # build dataframe of intersections
    # index: tuple of intersection coordinates
    # columns: list of indexes of roads that intersect at that intersection
    # values: number of roads that intersect at that intersection
    df = pd.DataFrame(index=intersections.keys(), columns=['intersection_coords', 'neighbors', 'road_indexes', 'num_roads'])
    for key in intersections:
        df.at[key, 'intersection_coords'] = key
        df.at[key, 'neighbors'] = intersections[key]["neighbors"]
        df.at[key, 'road_indexes'] = intersections[key]["roads"]
        df.at[key, 'num_roads'] = len(intersections[key]["roads"])
    return df

intersections = get_intersections(gdf)
df = get_dataframe(intersections)
sorted_intersections = df.sort_values(by=['num_roads'], ascending=False)

# get top 10 intersections
top_10_intersections = sorted_intersections.head(10)
print(top_10_intersections)
indexes = []
for i in range(len(top_10_intersections)):
    intersection = top_10_intersections.iloc[i]
    indexes += intersection['road_indexes']

# filter original dataframe to only include roads that intersect at first intersection
first_10_intersection_roads_df = gdf[gdf['OBJECTID'].isin(indexes)]

# plot roads that intersect at first intersection
plot(first_10_intersection_roads_df, "first_10_intersection_roads")

sorted_intersections.reset_index(drop=True, inplace=True)
# convert to geodataframe
sorted_intersections['geometry'] = sorted_intersections['intersection_coords'].apply(Point)
sorted_intersections = gpd.GeoDataFrame(sorted_intersections, geometry='geometry')
# convert fields to string
sorted_intersections['intersection_coords'] = sorted_intersections['intersection_coords'].astype(str)
sorted_intersections['road_indexes'] = sorted_intersections['road_indexes'].astype(str)
sorted_intersections['neighbors'] = sorted_intersections['neighbors'].astype(str)
# write to geojson
sorted_intersections.to_file('data/intersections.geojson', driver='GeoJSON', crs='epsg:3857')

# plot intersections
plot(sorted_intersections, "sorted_intersections")
          