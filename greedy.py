class Greedy:
    
    def __init__(self, instance):
        self.instance = instance
        self.concomp = [[i] for i in range(len(instance.dim()))]
        self.edges = []
        self.degree = {i: 0 for i in range(len(instance.dim()))]
        self.done = False

    def step(self):
        if self.done:
            return
        if len(self.concomp) == 1:
            nodes_with_degree_one = []
            for key, value in self.degree.items():
                if value == 1:
                    nodes_with_degree_one.append(key)
            p = nodes_with_degree_one[0]
            q = nodes_with_degree_one[1]
            self.edges.append((p, q))
            self.done = True
            return
            
        # Find the edge with the lowest cost, that is not yet chosen, does not
        # create a loop, and does not create nodes with degree higher than 2.
        min_dist = 9999999999
        best_edge = None
        for i in range(len(self.instance.get_dim())):
            for j in range(len(self.instance.get_dim())):
                if self.instance.get_dist(i, j) >= min_dist:
                    continue
                if self.degree[i] >= 2 or self.degree[j] >= 2:
                    continue
                if (i, j) in self.edges or (j, i) in self.edges:
                    continue
                is_connected = False
                for cc in self.concomp:
                    if i in cc and j in cc:
                        is_connected = True
                if is_connected:
                    continue
                best_edge = (i, j)
                min_dist = self.instance.get_dist(i, j)
        self.edges.append(best_edge)
        i, j = best_edge 
        self.degree[i] += 1
        self.degree[j] += 1
        for cc in self.concomp:
            if i in cc:
                concomp_of_i = cc
            if j in cc:
                concomp_of_j = cc
        self.concomp.remove(concomp_of_i)
        self.concomp.remove(concomp_of_j)
        self.concomp.append(concomp_of_i + concomp_of_j)

    def unstep(self):
        self.done = False
        if len(edges) > 0:
            self.edges.pop()
            return True
        return False
