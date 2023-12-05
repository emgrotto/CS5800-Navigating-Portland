

# Final Report: Navigating Portland

## Introduction
*a context that will help me understand your chosen topic, with a clearly-
defined question inspired by your issue with a rationale that explains what you are doing and why. I’d also like a couple of paragraphs where you tell me why this particular topic is important to you, and why each of you in the group is personally invested in answering this question.
NOTE: you can just copy and paste that section of your Final Project Proposal to form your
Introduction*

1.   Question:
Given Portland roads as the network we travel on. Can we determine optimal locations for a given number of bus stops, such that we are minimizing distance to amenities (schools, healthcare and grocery shops)?
 
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


## Analysis

*a description of the methods you used to gather your data and/or solve
your problem. What did you do and why? Show clear steps throughout every step of your
analysis, referencing specific topics/modules covered in the CS 5800 course. If you produced a
computer program (e.g. in Python/Java/C), make sure you submit the relevant computer
program as an Appendix to your .pdf report. I recognize that each report will be different, so I
will customize these 25 marks to align with the specific nature of your project.*


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

## References
1. Huitt, W. (2007). Maslow's hierarchy of needs. Educational Psychology Interactive. Valdosta, GA: Valdosta State University. Retrieved Nov 13, 2023 from, http://www.edpsycinteractive.org/topics/regsys/maslow.html
2. Greater Portland Transit District. (2023). 2023 Operating Budget. Retrieved Nov 13, 2023, from https://gpmetro.org/DocumentCenter/View/1497/2023-Operating-Budget--Approved-22323?bidId=
3. Google Maps. ( n.d.). [ Portland Bus Root Locations]. Retrieved December 1, 2023, from https://www.google.com/maps/d/edit?mid=1ndsALekiokpddnr-6D7I4t2-j3xU9xs&ll=43.67155787430646%2C-70.2770516&z=13
