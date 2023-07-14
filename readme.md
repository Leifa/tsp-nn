# Visualization of a heuristic for TSP (Travelling Salesman Problem)

![Preview picture](img/preview.png?raw=True)

Install pygame using `pip install pygame` and then run `main.py`.
Step through the algorithm using the arrow keys.

The algorithm calculates an initial solution for the TSP instance using the nearest neighbor heuristic, so it starts the tour at a random point and then greedily continues the tour by travelling to the nearest neighbor that is not yet visited.

The solution is then improved by looking at pairs of edges of the tour. If the current tour uses the edges (i, j) and (k, l), but using the edges (i, k) and (j, l) is cheaper, it swaps the first two for the second two edges. Note that this swap yields again a solution.
