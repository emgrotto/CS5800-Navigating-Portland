import geopandas as gpd
import pandas as pd
from shapely import wkt


groc = pd.read_csv('Portland Bus Route Locations- Grocery Stores.csv')
scho = pd.read_csv('Portland Bus Route Locations- Schools.csv')
hc = pd.read_csv('Portland Bus Route Locations- Healthcare Facilities.csv')
all = pd.concat([groc,scho,hc])
all['WKT'] = gpd.GeoSeries.from_wkt(all['WKT'])
