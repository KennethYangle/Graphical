import numpy as np
from swarms import Drone, Swarm, Unit, List

class Algorithm:
    def __init__(self):
        pass

    def ConstructList(self, H, I):
        len_I = len(I.drones)
        len_H = len(H.drones)
        T = List(H, "Task")
        W = List(I, "Worker")
        W.num = T.num = max(len_I, len_H)

        if len_I == len_H:
            # T.units = H.drones
            for d in H.drones:
                T.units.append(Unit(d, d.id, "Task"))
            # W.units = I.drones
            for d in I.drones:
                W.units.append(Unit(d, d.id, "Worker"))
        elif len_I < len_H:
            t = (len_H - 1) // len_I + 1
            # T.units = H.drones
            for d in H.drones:
                T.units.append(Unit(d, d.id, "Task"))
            cnt = 0
            for k in range(t):
                for i in range(len_I):
                    W.units.append(Unit(I.drones[i], cnt, "Worker"))
                    cnt += 1
                    if cnt >= len_H:
                        break
                if cnt >= len_H:
                        break
        else:
            t = (len_I - 1) // len_H + 1
            cnt = 0
            for k in range(t):
                for i in range(len_H):
                    T.units.append(Unit(H.drones[i], cnt, "Task"))
                    cnt += 1
                    if cnt >= len_I:
                        break
                if cnt >= len_I:
                        break
            # W.units = I.drones
            for d in I.drones:
                W.units.append(Unit(d, d.id, "Worker"))

        return T, W

    def GetNeighborhood(self, T, W, G):
        # calc WLs in dronei
        pass