import numpy as np

class Drone:
    def __init__(self, id, camp="", mu=[2.,3.,4.], sigma=[[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]]):
        self.id = id
        self.camp = camp
        self.mu = mu
        self.sigma = sigma
        self.position = np.random.multivariate_normal(self.mu, self.sigma)

    def __str__(self):
        return "id: {}; position: {};".format(self.id, self.position)


class Swarm:
    def __init__(self, num, camp="", area=[[0,0,10],[50,50,50]], sigma=[[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]], R=30):
        self.num = num
        self.camp = camp
        self.area = area
        self.sigma = sigma
        self.R = R
        self.drones = list()
        for i in range(self.num):
            mu = [np.random.uniform(area[0][0], area[1][0]), np.random.uniform(area[0][1], area[1][1]), np.random.uniform(area[0][2], area[1][2])]
            drone = Drone(id=i, camp=self.camp, mu=mu, sigma=self.sigma)
            self.drones.append(drone)
        if self.camp == "Interceptor":
            self.G0 = self.ConstructGraph()

    def __str__(self):
        prt = "Swarm: {}\n".format(self.camp)
        prt += "[drones]:\n"
        prt += "\n".join([d.__str__() for d in self.drones])
        prt += "\n"
        if self.camp == "Interceptor":
            prt += "[G0]:\n{}\n".format(self.G0)
        return prt

    def ConstructGraph(self):
        G = [[0 for i in range(self.num)] for j in range(self.num)]
        for i in range(self.num):
            G[i][i] = 1
            for j in range(i+1, self.num):
                d = np.linalg.norm(self.drones[i].position - self.drones[j].position)
                if d < self.R:
                    G[i][j] = G[j][i] = 1
        return G


class Unit(Drone):
    def __init__(self, drone, id, category=""):
        self.parent_id = drone.id
        self.camp = drone.camp
        self.mu = drone.mu
        self.sigma = drone.sigma
        self.position = drone.position
        self.id = id
        self.NWL = list()
        self.NTL = list()
        self.NTL_central  = list()
        if drone.camp == "Interceptor":
            self.category = "Worker"
        elif drone.camp == "Hostile":
            self.category = "Task"
        self.cohesion = 0.


class List(Swarm):
    def __init__(self, swarm, category=""):
        # base
        self.parent_num = swarm.num
        self.camp = swarm.camp
        self.area = swarm.area
        self.sigma = swarm.sigma
        self.R = swarm.R
        self.drones = swarm.drones
        if self.camp == "Interceptor":
            self.G0 = swarm.G0

        self.category = category
        self.units = list()
        self.num = 0
        self.center = np.array([0., 0., 0.])

    def __str__(self):
        prt = "List: {}\n".format(self.category)
        prt += "[units]:\n"
        prt += "\n".join([d.__str__() for d in self.units])
        prt += "\n"
        return prt

    def ConstructGraph(self):
        G = [[0 for i in range(self.num)] for j in range(self.num)]
        for i in range(self.num):
            G[i][i] = 1
            for j in range(i+1, self.num):
                d = np.linalg.norm(self.units[i].position - self.units[j].position)
                if d < self.R:
                    G[i][j] = G[j][i] = 1
        self.G = G
        return G
