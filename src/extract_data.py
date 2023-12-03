import requests
import pandas as pd
import geopandas as gpd
from shapely.geometry import shape, LineString
import contextily as ctx
import matplotlib.pyplot as plt


def get_gis_data():
    """
    This function fetches data from the Maine GIS website and returns a dataframe
    """

    # Base url to fetch data
    base_url = "https://gis.maine.gov/arcgis/rest/services/dot/MaineDOT_OpenData/MapServer/52/query"

    # Query parameters
    params = {
        'where': '1=1',
        'outFields': '*',
        'outSR': 3857,
        'f': 'json'
    }

    # initialize variables for paginating through data
    batch_size = 1000
    offset = 0

    # initialize lists to store data
    attributes = []
    geometry = []


    # iterate fetching batches of data, 1000 at a time until there is not more data left
    while True:
        params['resultOffset'] = offset
        response = requests.get(base_url, params=params)

        if response.status_code == 200:

            data = response.json()

            # Extract features from the response and add them to the result
            features = data.get('features', [])
            attributes.extend([feature.get("attributes", {}) for feature in features])
            geometry.extend([feature.get("geometry", {}) for feature in features])
            
            # break out of loop if this is the last batch of data
            if len(features) < batch_size:
                break
                
            offset += batch_size

        else:

            print(f"Failed to retrieve data. Status code: {response.status_code}")
            break

    # create dataframe with attributes and geometry data
    df = pd.DataFrame(attributes)
    df['geometry'] = geometry

    return df

def convert_to_line_string(geo):
    """
    This function converts the geometry column into a shapely LineString
    """
    path = [tuple(point) for point in geo['paths'][0]]
    return LineString(path)


# run main 
if __name__ == '__main__':
    # get data
    print('Fetching data...')
    data = get_gis_data()
    portland_df = data[data['townname'] == 'Portland']

    # convert geometry column into shapely format so that we can use geopandas
    print('Converting data to geopandas dataframe...')
    portland_df_copy = portland_df.copy()

    # convert geometry column into shapely LineString
    print('Converting geometry column to LineString...')
    portland_df_copy['geometry'] = portland_df_copy['geometry'].apply(convert_to_line_string)

    # create geopandas dataframe
    print('Creating geopandas dataframe...')
    portland_gdf = gpd.GeoDataFrame(portland_df_copy, geometry='geometry')

    # save geopandas dataframe to file
    print('Saving geopandas dataframe to file...')
    portland_gdf.to_file('data/portland_roads.geojson', driver='GeoJSON', crs='epsg:3857')

    ax = portland_gdf.plot(aspect=1, figsize=(60, 30), color="k")
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=15, crs=portland_gdf.crs)
    plt.savefig('figs/portland_roads.png')
