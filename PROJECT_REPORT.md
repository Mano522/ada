# Smart Traffic Signal Optimization Using Greedy Algorithm

## Problem Statement

Traffic congestion at road intersections increases waiting time, fuel consumption, and travel delay. Fixed-time traffic signals do not respond to changing vehicle density. This project uses a Greedy Algorithm to dynamically assign signal priority and green signal timing to the road with the highest vehicle count first.

## Objectives

- Represent a traffic intersection using graph concepts.
- Treat roads as graph edges and vehicle counts as edge weights.
- Apply a greedy strategy to select the busiest road first.
- Allocate higher green signal time to crowded roads.
- Display signal priority, optimized timings, and waiting time reduction through a Tkinter GUI.
- Build a beginner-friendly ADA mini-project suitable for VTU 5th semester presentation and viva.

## Algorithm Used

The project uses a Greedy Algorithm.

Algorithm steps:

1. Read vehicle counts for all roads.
2. Represent each road as an edge connected to the intersection node.
3. Sort roads in descending order of vehicle count.
4. Select the road with maximum traffic as the highest priority road.
5. Assign more green signal time to roads with more vehicles.
6. Continue assigning priority and green time until all roads are processed.
7. Display the optimized traffic order and estimated waiting time reduction.

Time complexity:

- Sorting `n` roads by vehicle count takes `O(n log n)`.
- Assigning signal time to all roads takes `O(n)`.
- Overall time complexity is `O(n log n)`.
- Space complexity is `O(n)`.

## System Architecture

The system has four main layers:

1. Input Layer: Tkinter input fields accept vehicle counts for each road.
2. Graph Layer: Roads are stored as graph edges with vehicle counts as weights.
3. Algorithm Layer: Greedy optimization sorts roads by traffic density and assigns signal timings.
4. Output Layer: The GUI displays priority order, green signal times, visual indicators, and waiting time reduction.

## Modules

- `Road`: Stores road name, source node, destination node, and vehicle count.
- `TrafficGraph`: Maintains the graph representation of the intersection.
- `GreedySignalOptimizer`: Applies the greedy algorithm and calculates signal timings.
- `TrafficSignalApp`: Builds the Tkinter GUI, validates input, displays the simulation, and shows results.

## Advantages

- Simple and easy to understand.
- Demonstrates a real-life use case of Greedy Algorithms.
- Dynamically prioritizes roads based on traffic density.
- Reduces waiting time compared with fixed signal timing.
- Uses graph concepts and weighted edges, making it relevant to ADA.
- Provides a visual GUI for better presentation and viva explanation.

## Limitations

- The waiting time calculation is an estimated simulation model.
- It considers one four-road intersection.
- It does not use live camera or sensor data.
- Emergency vehicles and pedestrian crossings are not included.
- Real-world traffic requires additional constraints such as lane width, road speed, and peak-hour patterns.

## Future Enhancements

- Add live traffic data using sensors or camera-based vehicle detection.
- Extend the graph to multiple connected intersections.
- Add emergency vehicle priority.
- Use machine learning to predict traffic density.
- Store historical traffic data for analysis.
- Add pedestrian crossing and public transport priority.

## Conclusion

This project demonstrates how a Greedy Algorithm can solve a practical traffic signal optimization problem. By selecting the road with maximum vehicles first and assigning it higher green signal time, the system improves traffic flow and reduces waiting time. Greedy Algorithms are widely used in resource allocation, scheduling, and optimization problems in real-world systems, making this project strongly relevant to VTU ADA concepts.

