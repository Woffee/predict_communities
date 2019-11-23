import pandas as pd
import os
import re
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

def simulate(save_path, nodes_num=100, classes_num=10):
    filepath = save_path + 'simulate_data2.csv'

    rand = np.random.randn(1, classes_num).flatten()
    classes = []
    for n in rand:
        n = int(abs(n * (nodes_num/classes_num)))
        classes.append(n)

    tmp = 0
    with open(filepath, 'w') as fw:
        for n in classes:
            for i in range(n):
                for j in range(n):
                    if i < j:
                        w = random.random()
                        u1 = i + tmp
                        u2 = j + tmp
                        fw.write( str(u1) + ',' + str(u2) + ',' + str(w) + "\n" )
            tmp = tmp + n
    print(tmp)
    return filepath



if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SAVE_PATH = BASE_DIR + '/data/'

    simulate_filepath = simulate(SAVE_PATH)
    print(simulate_filepath)