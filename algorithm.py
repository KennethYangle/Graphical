import numpy as np
from swarms import Drone, Swarm, List

class Algorithm:
    def __init__(self):
        pass

    def ConstructList(self, H, I):
        len_I = len(I.drones)
        len_H = len(H.drones)
        T = List(H, "Task")
        W = List(I, "Worker")
        W.num_unit = T.num_unit = max(len_I, len_H)

        if len_I == len_H:
            T.units = H.drones
            W.units = I.drones
        elif len_I < len_H:
            t = (len_H - 1) // len_I + 1
            T.units = H.drones
            for k in range(t):
                for i in range(len_I):
                    W.units.append(I.drones[i])     # Here is shallow copy, CAUTION !!!
                    if len(W.units) >= len_H:
                        break
                if len(W.units) >= len_H:
                        break
        else:
            t = (len_I - 1) // len_H + 1
            for k in range(t):
                for i in range(len_H):
                    T.units.append(H.drones[i])
                    if len(T.units) >= len_I:
                        break
                if len(T.units) >= len_I:
                        break
            W.units = I.drones

        return T, W