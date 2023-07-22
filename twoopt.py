class TwoOpt:
    
    def __init__(self, instance, tour):
        self.instance = instance
        self.tour = tour
        self.done = False
        self.swapstack = []

    def step(self):
        improvements = [[None for _ in range(len(self.tour)-1)] for _ in range(len(self.tour)-1)]
        for i in range(len(self.tour)-3):
            for j in range(i+2, len(self.tour)-1):
                p1 = self.tour[i]
                p2 = self.tour[i+1]
                p3 = self.tour[j]
                p4 = self.tour[j+1]
                # instead of p1-p2 and later p3-p4, we go p1-p3 and later p2-p4
                delta = -self.instance.get_dist(p1, p2)-self.instance.get_dist(p3, p4)+self.instance.get_dist(p1, p3)+self.instance.get_dist(p2, p4)
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
            self.done = True
        else:
            self.swapstack.append(best_index) 
            i, j = best_index 
            self.tour[i+1:j+1] = self.tour[i+1:j+1][::-1]

    def unstep(self):
        self.done = False
        if len(self.swapstack) > 0:
            i, j = self.swapstack.pop() 
            self.tour[i+1:j+1] = self.tour[i+1:j+1][::-1]
            return True
        else:
            return False

    def is_done(self):
        return self.done
