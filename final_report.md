

# Final Report: Navigating Portland
Authors: Emma Morse, Shuiming Chen, Amanda Haskell
## Introduction

### Question:
***Given Portland roads as the network we travel on. Can we determine optimal locations for a given number of bus stops, such that we are minimizing distance to amenities (schools, healthcare and grocery shops)?***
 
Shuiming chen:

Dijkstra's algorithm is used to find the shortest path between nodes in a graph, so maybe it is a great idea to apply this algorithm in our daily life.
 
Suppose we named the starting point as the student’s living area, and Hannaford Supermarket, Walmart, Trader Joe’s, Whole Foods Market, Roux institute, Maine Medical Center, Portland Museum of Art, Walgreens, CVS, Workout Anytime, Portland International Jetport, Portland Head Light, Old Port etc. as the end points, so that we can make a graph that covers most of public amenities that a roux institute student might going. And the weight edges of the map will be using the road lengths.
 
Why bus routes instead of driving routes?
We are trying to apply Dijkstra's algorithm in our real daily life. On the one hand, some students may not own a car, on the other hand, if students can drive a car, it would be kind of/relatively meaningless to apply this algorithm in Portland city because they can drive anywhere straightforward. When using bus routes, there are some amenities that the students cannot reach out straight, it will help to build the map that the start point may need some intersection point to reach out other end points.
 
Amanda:

Public transportation is a valuable resource to students, as discussed above. It’s also a valuable resource to those who have limited access to other modes of transportation. These may be physical limitations, financial limitations, or any number of other challenges.
All people have basic needs that must be met. This is a fundamental principle I frequently utilize as a healthcare worker, based on  Maslow’s hierarchy of needs<sup>1</sup>. First physiological needs must be met (food, shelter), then safety needs (health, family) and so on. We have chosen to develop an optimized public transportation route including locations like grocery stores, healthcare facilities, etc… as a way to meet the needs of the residents of Portland.

Emma:

Greater Portland’s primary public transportation system: GPMetro is an organization that is very tightly funded. In 2022 GPMetro’s annual budget was $13,144,976<sup>2</sup> and needed to seek out federal and state funding to maintain, upgrade or expand facilities. Because of this GPMetro struggles to expand or add routes due to the added cost of employees, buses and facility space. Nevertheless, the bus system has an annual ridership of almost 1.25 million (still recovering from COVID-19) making it a critical transportation option for Southern Mainers. 
Having researched this, it is clear that this is a precious resource that does not get the funding it needs. Being a pedestrian first resident of Portland, I have on many occasions attempted to use the bus system and found it to be both infrequent and bus-stops inconveniently placed for my desired destination. Without learning to drive and accepting the cost of car ownership there are unfortunately still areas of Portland and surrounding towns that are inaccessible to me. We cannot necessarily explore the issue of frequency in this project, however; I am interested to learn if the routes have been designed optimally. Are there alternative routes that are more efficient and hence cheaper to maintain?


## Analysis and Results

### Data Collection
We began our analysis by collecting data on the road systems in Maine. Data was retrieved from the Maine DOT open data arcgis server, and filtered to include only roads in the city of Portland. The data was saved such that location geometries were transformed into a X,Y format on a 2D plane- this was accomplished by using the EPSG 3857 coordinate system.

[Link to relevant source file](https://github.com/emgrotto/CS5800-Navigating-Portland/blob/main/src/extract_data.py)

**Portland Road Data Mapped**

![Alt text](figs/portland_roads.png?raw=true "Raw Portalnd Road Data Mapped")

Next we gathered data on priority locations utilizing Google maps. Location data for grocery stores, schools, and healthcare facilities was retrieved in WKT format, downloaded as separate csv files, then merged into one geodataframe. This location data was projected onto the same coordinate system used with the road system data.

[Link to relevant source file](https://github.com/emgrotto/CS5800-Navigating-Portland/blob/main/src/utils.py)

**Priority Locations Data Mapped**

![Alt text](figs/priority_locations.png?raw=true "Raw Portalnd Road Data Mapped")

### Data Transformation

The data collected from the MaineDOT contained road locations as linestrings. Our goal was to transform that data into a graph format so we could utilize the graph traversal algorithms learned in Module 5.

Nodes for the graph were created from road intersections. This was accomplished by extracting the beginning and ending coordinates of each road, creating a node at each of those locations if such as node did not already exist, or updating nodes that did already exist.
Weighted edges were created from the road segments between intersections, with a weight equal to the length of said segment.

Nodes and edges were stored in an adjacency list format, utilizing a nested Python dictionary data structure. The node(intersection) point coordinates were used as keys, with a dictionary as a value. The value dictionary includes the "neighbors" key, which is associated with a list of adjacent nodes(intersections). Additionally, road indexes, number or roads, and geometry data is stored in the nested dictionaries.

[Link to relevant source file](https://github.com/emgrotto/CS5800-Navigating-Portland/blob/main/src/build_intersection_data.py)

**Intersection Data Mapped**

![Alt text](figs/sorted_intersections.png?raw=true "Intersection Data Mapped")

Next, a graph was created utilizing the Networkx Python package. Networkx is a package designed specifically for building, utilizing and manipulating complex graphs/network structures.<sup>4</sup> 

This gave us an undirected, weighted graph with parameters shown below. As explained above, nodes are roda intersections, edges are road segments between intersections, and edge weights are the road segment lengths.



[Link to relevant source file](https://github.com/emgrotto/CS5800-Navigating-Portland/blob/main/src/utils.py)


**Road Data Graph Mapped**

![Alt text](figs/connected_components.png?raw=true "Road Data Graph")

**Graph Information**

```
Number of roads:  3607
Number of intersections:  2735

Graph information:
Number of nodes:  2735
Number of edges:  3548
Number of connected components:  7
max degree:  8
min degree:  1
```

Next we needed to identify which graph nodes to include in our ideal public transportation route.

We judged that the graph produced from the roads was dense enough that all priority locations would be within reasonable walking distance from a road intersection, so the planimetric distance from our priority location coordinates to the intersection coordinates would be a reasonable heuristic to use find priority graph nodes.

We utilized some of the principles learned in Module 8- dynamic programing and Modules 6 and 7- greedy algorithms to create an algorithm that compared each single high-priority point to all our graph nodes (storing each value rather than iterating), and ultimately selecting the nodes with the minimum distance from each priority location as the representative node for that location. This gave us a list of 32 high priority nodes to include in our path.

[Link to relevant source file](https://github.com/emgrotto/CS5800-Navigating-Portland/blob/main/locations%20data/locations_bus.py)


### Shortest Path Analysis

Our original plan to find the optimal transportation route connecting priority locations was to use a version of a shortest path algorithm selecting minimum distances between nodes.

We began by applying Dijkstra's algorithm via the Networkx.shorteset_path method, selecting a source node from our list of priority nodes. We quickly realized, while this will give us the shortest path between each other priority node and the source node, it did not generate a path that included ALL of the priority nodes. 

We considered apply Dijkstra's in a greedy stepwise manner: select the shortest distance between nodes in the priority node list, then select the node with the shortest path from the second node and so on, iterating through the remaining nodes in the priority node list. We realized, however, that this was not guaranteed to give us the shortest path between all nodes of the graph.

We then considered finding all the simple paths in the graph, filtering by only paths including our priority nodes, and selecting the path with the minimum cost. 

While this would have likely given us the optimal answer, we utilized the topics learned from Module 1 and judged the time complexity to be prohibitive as our graph has 2735 nodes and 3548 edges. This method would have a time complexity of O(n!) where n =  number of nodes in the graph.

Next we examined utilizing the Floyd-Warshall algorithm to generate the shortest path between all pairs of nodes in the graph, then finding the shortest weighted path between pairs of nodes in our priority node list. While generating the all pairs shortest paths would be reasonable to execute, finding the shortest path of our priority nodes would again very time complex. It would require finding all permutations of the priority nodes, calculating the path cost for each, and finding the minimum cost path among those. This also had a time complexity of O(n!).

As we continued to contemplate our problem, we recognized that it was very close in nature to the Traveling Salesman Problem (TSP) that we learned about in Module 11. Although we were not attempting to generate a Hamiltonian Cycle, we were seeking the minimum cost path that would take us through a set of nodes in a graph- essentially a TSP tour of a certain subset of the graph, without returning to the starting node. Since TSP in NP Complete, there is no way to generate an optimal output in polynomial time. This led us to conclude that the best method to find our ideal bus route would be to utilize the methods learned in Module 12 and generate an approximation algorithm for a modified TSP tour.

We were able to again to utilize the existing methods in the Networkx package and generate an approximate minimum cost path through all of our priority nodes. The approximation we utilized was a Metric Approximation, utilizing Christofides algorithm.

The Christofides algorithm begins by creating a minimum spanning tree (M) for the desired nodes. A set is created of odd-degree vertices (oV) from M. oV contains, at a minimum, all the leaf nodes of M and by the handshaking lemma, oV has an even number of vertices. A minimum weight perfect matching is made from the complete graph of oV. The edges of that matching are combined with the edges of M and a graph is formed with all nodes having an even degree. A Eulerian tour is made of the new graph. Duplicate nodes are removed from the path, generating an approximate minimum cost tour<sup>5</sup>.

Christofides algorithm, like other metric TSP algorithms, utilizes the triangle inequality to prove the validity of the tour that is generated. That is, for any 3 nodes in a complete weighted graph G(V,E) with non-negative with edges:



$\ (u,v),(v,w), (u,w)$

$\ c(u,w) <= c(u,v) + c(v,w)$


Since our graph is complete, has non-negative weigh edges, and is built on an X,Y coordinate plane, the triangle inequality does hold and the tour generated by removing duplicate nodes form the Eulerian tour is valid. Since the algorithm utilizes a minimum spanning tree, we know that each edge added to that tree is the minimum valued edge that connects the existing tree (starting from an empty tree) to the remaining nodes that are not yet in the tree. Such edges are added until no nodes remain unconnected. So we know that the tree that is generated both spans all nodes of our subgraph that includes priority nodes, and is a set of minimum valued edges spanning those nodes. So Christofides algorithm has generated an approximate shortest path between all our priority nodes.


When considering the execution of Metric TSP algorithms, we know that the cost of the MST generated by the approximation algorithm will always be less than or equal to the cost c of the optimal solution (OPT), as a MST can be generated by deleting any edge from a tour, and all edges are non- negative.

$\ c(MST) <= c(OPT)$ 

Since we are using a Eulerian tour (W) to traverse the MST, we will visit every edge/vertex exactly twice. So the cost for this walk will be equal to two times the cost of the tree itself

$\ c(W) = 2c(MST)$

Combining these two factors, we know that 

$\ c(W) <= 2*c(OPT)$

Since we know the triangle equality holds, then we know that the path that is generated when duplicate nodes are removed from W must have a value less than the W, so for our final resulting path $\ P $

$\ c(P) <= c(W) <= 2*c(OPT) \rightarrow c(P) <= 2*c(OPT)$ 

The Christofides further improves this approximation. 
Let us define:

$\ P $  to be the perfect matching of oV

$\ T' $ be the OPT TSP tour for G

$\ N' $ be the OPT TSP tour of oV

$\ R_1 , \ R_2$ to be two perfect matchings of oV on the edges of $\ N'$ taken alternately.

Then:

$\ c(P) = min \ c(R_1,R_2) $ 

as stated above

$\ c(P) \le \ c(N')/2$   
as the minium of R<sub>1</sub> and R<sub>2</sub> must be at most the average of the N'

$\ c(P) \le \ c(T')/2$ 

as T' is created from oV and thus only contains the G(V) with an odd number of edges and the triangle inequality tells us the cost of our tour will be no worse than $\ c(T')$  and $\ c(N')$ will be no worse than $\ c(T')$ as N' is the optimal tour on oV

When we combine the edges of P with the edges of the MST previously generated we have:

$\ c(P) \le \ c(T')/2$

$\ c(MST) \le c(T')$

$\ c(P) + c(MST) \le \ 3c(T')/2$

The Christofides tour has generated a 3/2 approximation of the optimal TSP tour. Since our "tour" is truly a path, there is one less edge than in a true TSP tour and is thus less costly, so clearly the approximation would also yield at least a 3/2 approximation of our path.

[Link to relevant source file](https://github.com/emgrotto/CS5800-Navigating-Portland/blob/main/src/shortest_path.py)


**Approximate Shortest Path All Priority Locations**

![Alt text](figs/shortest_path.png?raw=true "Shortest Path")


## Conclusion

*based on your analysis, answer your question. Then discuss the
weaknesses and limitations of your project and suggest avenues for future research. And finally,
conclude with a paragraph (one separate paragraph per group member) describing what you
learned from this project, and whether this report will be of any value to you – either for a
future Northeastern course, or for some other project or endeavour you wish to pursue upon
your graduation from Northeastern.
Please note: I will not give you a “page limit” because some reports will naturally be longer than others.
Your goal is to address each of the points listed above: if you do that, you will do very well on this Final
Project Report.*

Shuiming chen:

Amanda:

Emma:

## References
1. Huitt, W. (2007). Maslow's hierarchy of needs. Educational Psychology Interactive. Valdosta, GA: Valdosta State University. Retrieved Nov 13, 2023 from, http://www.edpsycinteractive.org/topics/regsys/maslow.html
2. Greater Portland Transit District. (2023). 2023 Operating Budget. Retrieved Nov 13, 2023, from https://gpmetro.org/DocumentCenter/View/1497/2023-Operating-Budget--Approved-22323?bidId=
3. Google Maps. ( n.d.). [ Portland Bus Root Locations]. Retrieved December 1, 2023, from https://www.google.com/maps/d/edit?mid=1ndsALekiokpddnr-6D7I4t2-j3xU9xs&ll=43.67155787430646%2C-70.2770516&z=13
4. Aric A. Hagberg, Daniel A. Schult and Pieter J. Swart, “Exploring network structure, dynamics, and function using NetworkX”, in Proceedings of the 7th Python in Science Conference (SciPy2008), Gäel Varoquaux, Travis Vaught, and Jarrod Millman (Eds), (Pasadena, CA USA), pp. 11–15, Aug 2008
5. N. Christofides, Worst-case analysis of a new heuristic for the travelling salesman prob- lem, Report 388, Graduate School of Industrial Administration, Carnegie Mellon Uni- versity, 1976.

***Not sure if needed***

5. Penninsula Transit Committee. (2008). Portland Peninsula Transit Study. Retrieved from https://content.civicplus.com/api/assets/c4e5ef98-a109-4021-890c-57c368d647d8


## Appendix
### Code
[Link to project GitHub repo](https://github.com/emgrotto/CS5800-Navigating-Portland/tree/main)