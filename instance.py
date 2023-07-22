import math

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

class Instance:
    def __init__(self, points):
        self.points = points
        self.dim = len(points)
        self.distances = [[None for _ in range(self.dim)] for _ in range(self.dim)]
        self.calculate_distances()

    def calculate_distances(self):
        for i in range(self.dim):
            for j in range(self.dim):
                self.distances[i][j] = distance(self.points[i], self.points[j])

    def get_dist(self, i1, i2):
        return self.distances[i1][i2]

    def get_tour_distance(self, tour):
        result = 0
        for i in range(len(tour)-1):
            result += self.get_dist(tour[i], tour[i+1])
        return result
    
    def get_dim(self):
        return self.dim

    def get_points(self):
        return self.points
