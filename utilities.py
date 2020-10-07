import sys
import pickle
import os

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
load_tree()

def format_path(path, path_type='folder'):
    if path == '.':
        path = './'
    if path[:2] != './':
        path = './' + path
    if path[-1] != '/' and path_type == 'folder':
        path = path + '/'
    return path


def check_parent_exist(path, tree):
    for i in range(len(path)-2, 0, -1):
        if path[i] == '/':
            break
    if path[:i+1] in tree.keys():
        return True
    return False