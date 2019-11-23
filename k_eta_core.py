"""

"""
import pandas as pd
import os
import re
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class k_eta_core:
    def __init__(self):
        G = nx.Graph()
        G.add_edge(0, 1, weight=0.5)
        G.add_edge(0, 2, weight=0.5)
        G.add_edge(1, 2, weight=0.5)
        G.add_edge(1, 5, weight=0.5)
        G.add_edge(2, 3, weight=0.5)
        G.add_edge(2, 4, weight=0.5)
        G.add_edge(2, 5, weight=0.5)
        G.add_edge(2, 6, weight=0.5)
        G.add_edge(3, 4, weight=0.5)
        G.add_edge(3, 6, weight=0.5)
        G.add_edge(3, 7, weight=0.5)
        G.add_edge(4, 6, weight=0.5)
        G.add_edge(4, 7, weight=0.5)
        G.add_edge(5, 6, weight=0.5)
        G.add_edge(5, 8, weight=0.5)
        G.add_edge(6, 7, weight=0.5)
        G.add_edge(6, 8, weight=0.5)

        # print(G.edges(8))
        # for (u, v, wt) in G.edges.data('weight'):
        #     print(u,v,wt)
        # print(G[1][2]['weight'])
        # adj = list(G.neighbors(1))

        self.G = G


    # T(j, N_v)
    def deg_t(self, v, j, adj):
        res = 0.0
        for u in adj:
            w = self.G[v][u]['weight']
            res = res + (1.0*w/(1-w)) ** j
        # print("deg_t:", res)
        return res

    # R(i, N_v)
    def deg_r(self, v, i, adj):
        if i==0:
            return 0
        if i==1:
            res = 0
            for u in adj:
                w = self.G[v][u]['weight']
                res = res + (1.0 * w / (1 - w))
            # print("res=", res)
            return res

        res = 0
        for j in range(1, i + 1):
            tmp = (-1) ** (j+1)
            t = self.deg_t(v, j, adj)
            r = self.deg_r(v, i-j, adj)
            res = res + 1.0 * tmp * t * r
            # print("sub res:", res)
        res = res/i
        # print("res:", res)
        return res

    # Pr[ deg(v)=x ]
    def pr_deg(self, v, i):
        adj = list(self.G.neighbors(v))
        P_v = 1.0
        for u in adj:
            w = self.G[v][u]['weight']
            P_v = P_v * (1-w)

        R = self.deg_r(v, i, adj)
        # print("P_v:", P_v)
        # print("R:", R)
        return P_v * R

    # eta_deg(v)
    def eta_deg(self, v, eta):
        adj = list(self.G.neighbors(v))
        kk = 0
        p_max = 0
        for k in range(len(adj)):
            # calculate Pr[deg(v) >= k]
            pr_deg_k = 1.0
            for i in range(k):
                pr_deg_k = pr_deg_k - self.pr_deg(v, i)
            print(v , k)
            print("pr_deg_k:", pr_deg_k)
            if pr_deg_k >= eta and pr_deg_k > p_max:
                p_max = pr_deg_k
                kk = k
        return kk

    # (k,eta)-cores
    def cores(self, k, eta):
        deg = {}
        D = {}
        c = {}
        max_deg = 0
        print("calculating eta_deg...")
        for v in self.G.nodes:
            tmp = self.eta_deg(v, eta)
            if tmp > max_deg:
                max_deg = tmp
            deg[v] = tmp
            vv = [v]
            if tmp in D.keys():
                D[tmp] = list(set(D[tmp]).union(set(vv)))
            else:
                D[tmp] = vv

        print("updating...")
        print("deg:", deg)
        print("D:", D)
        for k in range(max_deg+1):
            while k in D.keys() and D[k] != []:
                v = D[k].pop()
                c[v] = k
                adj = list(self.G.neighbors(v))
                for u in adj:
                    if deg[u]>k:
                        # recompute eta-deg(u)
                        tmp = self.eta_deg(v, eta)
                        D[deg[u]].remove(u)
                        D[tmp].append(u)
                        deg[u] = tmp
                self.G.remove_node(v)
        return c

    def show(self):
        pos = nx.spring_layout(self.G)
        nx.draw_networkx_nodes(self.G, pos, node_size=100, node_color="g")
        nx.draw_networkx_edges(self.G, pos, width=1, )
        nx.draw_networkx_labels(self.G, pos, font_size=10)
        plt.show()



if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SAVE_PATH = BASE_DIR + '/data/'

    kcore = k_eta_core()
    c = kcore.cores(3, 0.01)
    print(c)


    # test = [
    #     [0, 2],
    #     [1, 2],
    #     [2, 3],
    #     [5, 2],
    # ]
    # for row in test:
    #     v = row[0]
    #     i = row[1]
    #
    #     k = kcore.eta_deg(v, 0.01)
    #     print("eta deg(%d)=" % v, k)
