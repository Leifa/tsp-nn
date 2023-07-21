import math

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

PHASE_MIN = 0
PHASE_IMPROVE = 1
PHASE_DONE = 2

class Algo:
    
    def __init__(self, points):
        self.points = points
        self.dim = len(points)
        self.distances = [[None for _ in range(self.dim)] for _ in range(self.dim)]
        self.calculate_distances()
        self.concomp = [[p] for p in self.points]
        self.edges = []
        self.degree = {p: 0 for p in self.points}
        self.phase = PHASE_MIN
        self.swapstack = []

    def calculate_distances(self):
        for i in range(self.dim):
            for j in range(self.dim):
                self.distances[i][j] = distance(self.points[i], self.points[j])

    def get_tour_distance(self):
        result = 0
        for p, q in self.edges:
            result += distance(p, q)
        return result

    def step(self):
        if self.phase == PHASE_MIN:
            self.step_min()

    def step_min(self):
        print(self.concomp)
        print(self.degree)
        if len(self.concomp) == 1:
            nodes_with_degree_one = []
            for key, value in self.degree.items():
                print(f"{key}: {value}")
                if value == 1:
                    nodes_with_degree_one.append(key)
                print(nodes_with_degree_one)
            p = nodes_with_degree_one[0]
            q = nodes_with_degree_one[1]
            self.edges.append((p, q))
            self.phase = PHASE_DONE
            return
            
        # Find the edge with the lowest cost, that is not yet chosen, does not
        # create a loop, and does not create nodes with degree higher than 2.
        min_dist = 9999999999
        best_edge = None
        for i in range(len(self.points)):
            p = self.points[i]
            for j in range(len(self.points)):
                q = self.points[j]
                if self.distances[i][j] >= min_dist:
                    continue
                if self.degree[p] >= 2 or self.degree[q] >= 2:
                    continue
                if (p, q) in self.edges or (q, p) in self.edges:
                    continue
                is_connected = False
                for cc in self.concomp:
                    if p in cc and q in cc:
                        is_connected = True
                if is_connected:
                    continue
                best_edge = (p, q)
                min_dist = self.distances[i][j]
        self.edges.append(best_edge)
        p, q = best_edge 
        self.degree[p] += 1
        self.degree[q] += 1
        for cc in self.concomp:
            if p in cc:
                concomp_of_p = cc
            if q in cc:
                concomp_of_q = cc
        self.concomp.remove(concomp_of_p)
        self.concomp.remove(concomp_of_q)
        self.concomp.append(concomp_of_q + concomp_of_p)

