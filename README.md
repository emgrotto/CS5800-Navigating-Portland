# Navigating Portland

CS5800 final semester project 

# link to checkpoints:

* [project proposal](./project_proposal.md)
* [final report](./final_report.md)

# Description of src files

### [extract_data.py](./src/extract_data.py)

This script get road geometry data from the Maine DOT open data arcgis server and saves Portland data as a geojson in EPSG 3857. EPSG 3857 is a coordinate system in 2D where the coordinates are transformed to X, Y in a 2D plane.

This script writes to [data/portland_roads.geojson](./data/portland_roads.geojson).

### [plot_raw_data.py](./src/plot_raw_data.py)

This script reads in [data/portland_roads.geojson](./data/portland_roads.geojson) and plots the geometries we a basemap. Saving it to [figs/portland_roads.png](./figs/portland_roads.png).

### [build_intersection_data.py](./src/build_intersection_data.py)

This script wrangles the portland road data in [data/portland_roads.geojson](./data/portland_roads.geojson) to get a intersections. This is helpful to learn more, verify and plot the data. The intersections are writen to the [data/intersections.geojson](./data/intersections.geojson) file with:

* intersection coordinates
* list of connected roads (as `OBJECTID` in [data/portland_roads.geojson](./data/portland_roads.geojson))
* list of adjacent intersections
* number of connected roads

It also plots and saves 3 figures:

* A figure of all roads labeled `CONGRESS ST` as [figs/congress.png](./figs/congress.png) on a basemap
* A figure of all intersections as [figs/sorted_intersections.png](./figs/sorted_intersections.png) on a basemap
* A figure with the top 10 intersections (sorted by number of connected roads) as [figs/first_10_intersection_roads.png](./figs/first_10_intersection_roads.png) on a basemap

### [load_graph.py](./src/load_graph.py)

This script reads in [data/portland_roads.geojson](./data/portland_roads.geojson)) and [data/intersections.geojson](./data/intersections.geojson) data. It used the road data to populate a [NetworkX](https://networkx.org/documentation/latest/tutorial.html) graph and the intersection data to validate graph info.

It then plots each connected component of the graph as different colors onto a basemap. We have multiple connected components as Portland has islands! This plot is saved to [figs/connected_components.png](./figs/connected_components.png). For this project we will only focus on the largest connected component as it contains the roads of mainland Portland!

### [utils.py](./src/utils.py)

This script provides 3 helper functions:

* function to return geodataframes for data in [data/portland_roads.geojson](./data/portland_roads.geojson)), [data/intersections.geojson](./data/intersections.geojson) data and the 3 bus route location files in `data/`. 
* function that creates and returns a [NetworkX](https://networkx.org/documentation/latest/tutorial.html) graph from road data.
* function that returns the largest component of a graph.

### [shortest_path.py](./src/shortest_path.py)

This script uses the roads graph provided by [utils.py](./src/utils.py) and finds the shortest path containing all nodes closest to the locations defined by the 3 bus route location files in `data/` using [NetworkX.tsp](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.approximation.traveling_salesman.traveling_salesman_problem.html). It also plots the path on a basemap saved to [figs/shortest_path.png](./figs/shortest_path.png)
