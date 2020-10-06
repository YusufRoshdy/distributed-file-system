from flask import Flask, redirect, url_for, request
import sys
import pickle
import os

app = Flask(__name__)

tree = {'./': 1}

def save_tree():
    with open('tree.pkl', 'wb') as f:
        pickle.dump(tree, f, pickle.HIGHEST_PROTOCOL)

def load_tree():
    global tree
    if not os.path.isfile('tree.pkl'):
        print('Initializeing tree')
        with open('tree.pkl', 'wb') as f:
            pickle.dump(tree, f, pickle.HIGHEST_PROTOCOL)
    with open('tree.pkl', 'rb') as f:
        # print(pickle.load(f))
        tree =  pickle.load(f)
load_tree()

def format_path(path):
    if path[:2] != './':
        path = './' + path
    if path[-1] != '/':
        path = path + '/'
    return path


@app.route('/ls',methods = ['GET'])
def ls():
    path = request.form['path']
    path = format_path(path)

    ret = []
    if path not in tree.keys():
        return path + ' is not a directory'
    for t in tree:
        if path in t and len(path) != len(t):
            ret.append(t[len(path):])
    return '\n'.join(ret)

@app.route('/mkdir',methods = ['POST'])
def mkdir():
    global tree
    path = request.form['path']
    
    path = format_path(path)
    print(path)

    if path in tree.keys():
        return path + ' already exist'
    names = path.split('/')
    print(names)
    print(tree)
    if '/'.join([*names[:-2], '']) not in tree.keys():
        return "Parent directory doesn't exist"
    tree[path] = 1
    return 'sucsess'

if __name__ == '__main__':
   app.run(host=sys.argv[1], port=int(sys.argv[2]), debug = True)

