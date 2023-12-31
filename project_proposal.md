# Final Project Proposal
 
 
1.   Question:

Given Portland roads as the network we travel on. Can we determine optimal locations for a given number of bus stops, such that we are minimizing distance to amenities (schools, healthcare and grocery shops)?
 
2.   Context:

Shuiming chen

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

 
3.   A framework of our project:

Using open-source data reported by Maine DOT, create a graph representation of Portland roads using the distance of the roads as edge weights.
Either manually or programmatically get key amenity locations.
We can then supplement vertex values using an amenity proximity metric. This can be achieved using Dijkstra's (or maybe all source Algorithm)
Find a Subset of the graph that optimizes bus stop locations.
Using MSTs, find bus routes that are optimal connecting up all the bus stop locations.

We will be splitting the work on final project slides and other deliverables, utilizing a GitHub repository to collaborate.

4.   Scope:

The scope of our project will be limited to a specific geographic area. We are planning on using all of Portland, but depending on the availability and volume of data we may elect to limit the size of the geographic area to a smaller subsection of Portland, or possibly another smaller metropolitan area in Maine.
We will not examine every possible location a resident could wish to visit via public transportation, but rather focus on locations that provide necessary resources and/or that we judge likely to be of high value to riders.
We have also elected not to examine walking distance from the bus stop to the specific destinations.
 
 
5.   What we have accomplished so far and what is our plan going forward?
 
We have brainstormed ideas for high priority locations for bus stops/graph vertices and have developed a general framework/idea on which algorithms to apply and how to apply those algorithms.
We have confirmed that we are able to gather data on Portland road segments, however we still need to convert it into a graph-like format so that we can begin designing the algorithms.
 
 
6. Team members:

Amanda Haskell
haskell.am@northeastern.edu
 
Emma Morse
morse.e@northeastern.edu
 
Shuiming Chen
chen.shui@northeastern.edu
 
 
References:
1. Huitt, W. (2007). Maslow's hierarchy of needs. Educational Psychology Interactive. Valdosta, GA: Valdosta State University. Retrieved Nov 13, 2023 from, http://www.edpsycinteractive.org/topics/regsys/maslow.html
2. Greater Portland Transit District. (2023). 2023 Operating Budget. Retrieved Nov 13, 2023, from https://gpmetro.org/DocumentCenter/View/1497/2023-Operating-Budget--Approved-22323?bidId=