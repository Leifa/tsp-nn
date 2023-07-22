class NearestNeighbor:
    
    def __init__(self, instance):
        self.instance = instance
        self.tour = [0]
        self.done = False

    def step(self):
        if self.done:
            return
        if len(self.tour) == self.instance.get_dim():
            self.tour.append(self.tour[0])
            self.done = True
            return
        lowest_distance = 99999999
        current = self.tour[-1]
        nearest_neighbor = None
        for i in range(len(self.instance.get_points())):
            if i not in self.tour:
                distance_to_i = self.instance.get_dist(current, i)
                if distance_to_i < lowest_distance:
                    nearest_neighbor = i
                    lowest_distance = distance_to_i
        self.tour.append(nearest_neighbor)

    def unstep(self):
        self.done = False
        if len(self.tour) > 1:
            self.tour.pop()
            return True
        else:
            return False

    def is_done(self):
        return self.done

    def get_tour(self):
        return self.tour
