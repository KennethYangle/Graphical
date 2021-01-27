import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from main import GTA

class Theater:
    def __init__(self, gta):
        self.gta = gta
        self.fig = plt.figure(1)
        self.ax = plt.axes(projection='3d')
    def render(self):
        for t in self.gta.TL.units:
            self.ax.scatter(t.position[0], t.position[1], t.position[2], marker="*")
            self.ax.text(t.position[0], t.position[1], t.position[2], t.id)
        for w in self.gta.WL.units:
            self.ax.scatter(w.position[0], w.position[1], w.position[2], marker="o")
            self.ax.text(w.position[0], w.position[1], w.position[2], w.id)
        self.ax.scatter(self.gta.WL.center[0], self.gta.WL.center[1], self.gta.WL.center[2], marker="^")
        for i in range(self.gta.WL.num):
            for j in range(i+1, self.gta.WL.num):
                if self.gta.G[i][j] == 1:
                    self.ax.plot([self.gta.WL.units[i].position[0], self.gta.WL.units[j].position[0]], 
                                 [self.gta.WL.units[i].position[1], self.gta.WL.units[j].position[1]], 
                                 [self.gta.WL.units[i].position[2], self.gta.WL.units[j].position[2]])

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        # self.ax.set_ylim(-50, 100)
        self.fig.savefig("1.png", dpi=600)
        plt.show()