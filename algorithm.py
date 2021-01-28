import numpy as np
from swarms import Drone, Swarm, Unit, List
from itertools import permutations
from collections import deque

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

    def GetNeighborhood(self, T, W):
        pos_sum = np.array([0., 0., 0.])
        for i in range(W.num):
            pos_sum += W.units[i].position
        W.center = pos_sum / W.num

        pos_sum = np.array([0., 0., 0.])
        for i in range(T.num):
            pos_sum += T.units[i].position
        T.center = pos_sum / T.num

        # calc NWLs in uniti
        for i in range(W.num):
            for j in range(W.num):
                if W.G[i][j] == 1:
                    W.units[i].NWL.append({"id":j})
            print("NeighborWL {}: {}".format(i, W.units[i].NWL))

        # calc NTLs in uniti
        direction = T.center - W.center
        direction /= np.linalg.norm(direction)
        print("direction: {}".format(direction))
        for i in range(W.num):
            for j in range(T.num):
                di = T.units[j].position - W.units[i].position
                if di.dot(direction) / np.linalg.norm(di) > 0.98:   # cos theta
                    W.units[i].NTL_central.append({"id":j})
                if di.dot(direction) / np.linalg.norm(di) > 0.95:   # cos theta
                    W.units[i].NTL.append({"id":j})
            print("NeighborTL_central {}: {}".format(i, W.units[i].NTL_central))
            print("NeighborTL {}: {}".format(i, W.units[i].NTL))

    def CalcPayoff(self, T, W, M):
        for i in range(W.num):
            for t in W.units[i].NTL:
                t["payoff"] = M - np.linalg.norm(W.units[i].position - T.units[t["id"]].position)
            print("NeighborTL {}: {}".format(i, W.units[i].NTL))

    def CalcCE(self, u: Unit, W):
        per = permutations([i for i in range(len(u.NTL_central))], len(u.NWL))  # p[i] means u.NWL[i]["id"] choose u.NTL_central[p[i]]
        maxv = -1e10
        maxp = None
        for p in per:
            ulocal = 0
            for i, v in enumerate(p):
                # find payoff
                # print(W.units[u.NWL[i]["id"]].NTL)
                for tl in W.units[u.NWL[i]["id"]].NTL:
                    if tl["id"] == u.NTL_central[v]["id"]:
                        ulocal += tl["payoff"]
                        break
            # print("unit {}: p: {}, ulocal: {}".format(u.id, p, ulocal))
            if ulocal > maxv:
                maxv = ulocal
                maxp = p

        for i in range(len(u.NWL)):
            if u.NWL[i]["id"] == u.id:
                idx = i

        if maxp is not None:
            print("unit {} choose task {}".format(u.id, maxp[idx]))

    def SolveGG(self, T, W):
        for i in range(W.num):
            W.units[i].cohesion = np.linalg.norm(W.units[i].position - W.center)
        W.units.sort(key=lambda x: (x.cohesion))
        print(W)

        root = TreeNode(W.units[0])
        open_table = deque()
        open_table.append(root)
        close_table = []
        while len(open_table) != 0:
            r = open_table.popleft()
            close_table.append(r)
            for i in range(W.num):
                tmpid = W.units[i].id
                if W.G[r.val.id][tmpid] == 1 and tmpid not in [a.val.id for a in close_table] and tmpid not in [a.val.id for a in open_table]:
                    c = TreeNode(W.units[i], children=list())
                    r.children.append(c)
                    open_table.append(c)
                    print("node {} got unit {}".format(r.val.id, tmpid))
            print(r.val.id, [c.val.id for c in r.children])

        # View Tree Struct
        stash = deque()
        stash.append(root)
        while len(stash) != 0:
            r = stash.popleft()
            print("node {}:".format(r.val.id), end=" ")
            for c in r.children:
                stash.append(c)
                print(c.val.id, end=", ")
            print()

        # direct allocation
        print("<-- direct allocation -->")
        for i in range(W.num):
            self.CalcCE(W.units[i], W)


class TreeNode:
    def __init__(self, val=None, children=list()):
        self.val = val
        self.children = children