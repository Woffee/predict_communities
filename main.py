"""

"""
import pandas as pd
import os
import re
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def my_split(str):
    arr = str.split(',')
    res = []
    for item in arr:
        item = item.strip(' "')
        res.append(item)
    return ",".join(res)

def get_id(str):
    arr = str.split(',', 1)
    if len(arr)>1:
        return arr[0].strip(' "')
    return ''

def clean_data_1(filepath, save_path):
    new_filepath = save_path + 'data_only_friends.csv'
    # if os.path.exists(new_filepath):
    #     return new_filepath

    with open(filepath, 'r') as f:
        with open(new_filepath, 'w') as fw:
            for line in f.readlines():
                line = line.strip()
                id = get_id(line)
                arr = (re.findall('\[(.*?)\]', line))
                if len(arr)>1:
                    friends = my_split(arr[1])
                    fw.write(id + "," + friends + "\n")

    return new_filepath

def clean_data_2(filepath, save_path):
    new_filepath = save_path + 'data_cleaned.csv'
    if os.path.exists(new_filepath):
        return new_filepath

    i = 0
    data = {}
    with open(filepath, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            arr = line.split(',')
            id = arr[0]
            friends = arr[1:]
            data[id] = friends

    # print(data)
    print(len(data))

    new_filepath = save_path + 'data_cleaned.csv'
    with open(new_filepath, 'w') as fw:
        i = 0
        for u1, f1 in data.items():
            print("now: ", i)
            for u2, f2 in data.items():
                if u1 == u2:
                    continue
                same = set(f1) & set(f2)
                all  = set(f1) | set(f2)
                # print(len(same), len(all))
                s = u1 + "," + u2 + "," + str(1.0*len(same)/len(all))
                # print(s)
                fw.write(s + "\n")
            i = i + 1
    return new_filepath

def show(data):
    points = []
    edgelist = []

    for row in data.values:
        id = row[0]
        row[1] = row[1].strip(' "')
        friends = row[1].split(",")
        points.append(id)
        print(id, len(friends))
        for uid in friends:
            points.append(uid)
            edgelist.append((id, uid))
        # print(id, friends)
    # exit(0)

    G = nx.Graph()
    G.add_nodes_from(points)
    G = nx.Graph(edgelist)
    # pos = nx.spring_layout(G)
    # position = nx.circular_layout(G)
    position = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, position, node_size=10, nodelist=points, node_color="r")
    nx.draw_networkx_edges(G, position)
    # nx.draw_networkx_labels(G, position)
    plt.show()


def read_data(filepath):
    data = []

    G = nx.Graph()
    labels = {}

    with open(filepath, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            arr = line.split(',')
            if len(arr)>2:
                G.add_edge( arr[0], arr[1], weight=float(arr[2]) )
                labels[(arr[0],arr[1])] = arr[2]

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=5, node_color="r")
    nx.draw_networkx_edges(G, pos, width=1, )
    # nx.draw_networkx_labels(G, pos, font_size=8)
    # nx.draw_networkx_edge_labels(G, pos, labels, font_size=1)
    plt.show()

    return []

if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SAVE_PATH = BASE_DIR + '/data/'

    filepath = SAVE_PATH + 'simulate_data.csv'
    data = read_data(filepath)


    # new_filepath = clean_data_2(filepath, SAVE_PATH)
    # print(new_filepath)

    # data = pd.read_csv(new_filepath)
    # data = data[['id', 'friends']]

    # show(data)

