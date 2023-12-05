import pandas as pd
import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt

# read in data from geojson and plot with a basemap
gdf = gpd.read_file('data/portland_roads.geojson')
ax = gdf.plot(aspect=1, figsize=(60, 30), color="k")
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=15, crs=gdf.crs)
plt.suptitle('Portland Roads', fontsize=20)
plt.savefig('figs/portland_roads.png')
