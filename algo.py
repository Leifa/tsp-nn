import math

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

PHASE_NEAREST_NEIGHBOR = 0
PHASE_IMPROVE = 1
PHASE_DONE = 2

class Algo:
    
    def __init__(self, points):
        self.points = points
        self.dim = len(points)
        self.distances = [[None for _ in range(self.dim)] for _ in range(self.dim)]
        self.calculate_distances()
        self.tour = [0]
        self.phase = PHASE_NEAREST_NEIGHBOR

    def calculate_distances(self):
        for i in range(self.dim):
            for j in range(self.dim):
                self.distances[i][j] = distance(self.points[i], self.points[j])

    def step(self):
        if self.phase == PHASE_NEAREST_NEIGHBOR:
            self.step_nearest_neighbor()
        else:
            self.step_improve()

    def step_nearest_neighbor(self):
        if len(self.tour) == self.dim:
            self.tour.append(self.tour[0])
            self.phase = PHASE_IMPROVE
            return
        lowest_distance = 99999999
        current = self.tour[-1]
        nearest_neighbor = None
        for i in range(len(self.points)):
            if i not in self.tour:
                distance_to_i = self.distances[current][i]
                if distance_to_i < lowest_distance:
                    nearest_neighbor = i
                    lowest_distance = distance_to_i
        self.tour.append(nearest_neighbor)

    def step_improve(self):
        improvements = [[None for _ in range(len(self.tour)-1)] for _ in range(len(self.tour)-1)]
        for i in range(len(self.tour)-3):
            for j in range(i+2, len(self.tour)-1):
                p1 = self.tour[i]
                p2 = self.tour[i+1]
                p3 = self.tour[j]
                p4 = self.tour[j+1]
                # instead of p1-p2 and later p3-p4, we go p1-p3 and later p2-p4
                delta = -self.distances[p1][p2]-self.distances[p3][p4]+self.distances[p1][p3]+self.distances[p2][p4]
                improvements[i][j] = delta
        # find most negative value
        best_index = None
        best_delta = -0.000000001
        for i in range(len(self.tour)-3):
            for j in range(i+2, len(self.tour)-1):
                delta = improvements[i][j]
                if delta is not None:
                    if delta < best_delta:
                        best_delta = delta
                        best_index = (i, j)
        if best_index == None:
            self.phase = PHASE_DONE
        else:
            i, j = best_index 
            self.tour[i+1:j+1] = self.tour[i+1:j+1][::-1]
