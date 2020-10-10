import sys
import pickle
import os
import requests

def save_tree(tree):
    with open('tree.pkl', 'wb') as f:
        pickle.dump(tree, f, pickle.HIGHEST_PROTOCOL)

def load_tree():
    tree = {'./': 1}
    if not os.path.isfile('tree.pkl'):
        print('Initializeing tree')
        with open('tree.pkl', 'wb') as f:
            pickle.dump(tree, f, pickle.HIGHEST_PROTOCOL)
    with open('tree.pkl', 'rb') as f:
        # print(pickle.load(f))
        tree =  pickle.load(f)
    return tree

def save_pool(pool):
    with open('pool.pkl', 'wb') as f:
        pickle.dump(pool, f, pickle.HIGHEST_PROTOCOL)

def load_pool():
    pool = []
    if not os.path.isfile('pool.pkl'):
        print('Initializeing pool')
        with open('pool.pkl', 'wb') as f:
            pickle.dump(pool, f, pickle.HIGHEST_PROTOCOL)
    with open('pool.pkl', 'rb') as f:
        # print(pickle.load(f))
        pool =  pickle.load(f)
    return pool

def update_pool(pool):
    down = []
    for server in pool:
        try:
            print('pinging',  f'http://{server["ip"]}:{server["port"]}')
            r = requests.get(f'http://{server["ip"]}:{server["port"]}/check_up/')
        except Exception as e:
            down.append(server)
    for server in down:
        pool.remove(server)
    save_pool(pool)
    return pool

def format_path(path, path_type='folder'):
    # turn . to ./
    if path == '.':
        path = './'
    # add ./ to the start of path if doesn't exist
    if path[:2] != './':
        path = './' + path
    # add / to folder names
    if path[-1] != '/' and path_type == 'folder':
        path = path + '/'
    # remove / from the end of file name 
    if path_type == 'file':
        while len(path) and path[-1]=='/':
            path = path[:-1]
    return path


def check_parent_exist(path, tree):
    for i in range(len(path)-2, 0, -1):
        if path[i] == '/':
            break
    if path[:i+1] in tree.keys():
        return True
    return False