import numpy as np
random_seed = 367528110
if random_seed < 0:
    random_seed = np.random.randint(1<<32-1)
np.random.seed(random_seed)
print("random_seed: {}".format(random_seed))

from swarms import Drone, Swarm, Unit, List
from algorithm import Algorithm

class GTA:
    def __init__(self):
        self.IS = Swarm(10, camp="Interceptor", area=[[0,0,10],[50,50,50]])
        self.HS = Swarm(10, camp="Hostile", area=[[100,100,10],[150,150,50]])
        print(self.IS)
        print(self.HS)
        self.algs = Algorithm()
        self.TL, self.WL = self.algs.ConstructList(self.HS, self.IS)
        print(self.TL)
        print(self.WL)
        self.G = self.WL.ConstructGraph()
        print(self.G)
        self.algs.GetNeighborhood(self.TL, self.WL)
        self.algs.CalcPayoff(self.TL, self.WL, M=200)
        self.algs.SolveGG(self.TL, self.WL)

    def main(self):
        from plot import Theater
        theater = Theater(self)
        theater.render()

if __name__ == "__main__":
    gta = GTA()
    gta.main()