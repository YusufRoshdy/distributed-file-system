from flask import Flask, redirect, url_for, request
import sys
import pickle
import os
from utilities import *

app = Flask(__name__)

tree = load_tree()

@app.route('/ls',methods = ['GET'])
def ls():
    path = request.form['path']
    path = format_path(path, 'folder')

    ret = []
    if path not in tree.keys():
        return path + ' is not a directory'
    for t in tree:
        if path in t and len(path) != len(t):
            if t[len(path):][-1] == '/' or '/' not in t[len(path):]:
                ret.append(t[len(path):])
    return '\n'.join(ret)

@app.route('/mkdir',methods = ['PUT'])
def mkdir():
    global tree
    path = request.form['path']
    
    path = format_path(path, 'folder')

    if path in tree.keys():
        return path + ' already exist'
    
    if not check_parent_exist(path, tree):
        return "Parent directory doesn't exist"

    tree[path] = 1
    save_tree(tree)
    # TODO: send the command to the servers
    return 'sucsess'

@app.route('/touch',methods = ['PUT'])
def touch():
    global tree
    path = request.form['path']
    path = format_path(path, 'file')

    if path in tree.keys():
        return path + ' already exist'

    if not check_parent_exist(path, tree):
        return "Parent directory doesn't exist"
    
    # TODO: send the command to the servers and edit tree[path] = [??]
    tree[path] = 1
    save_tree(tree)
    return 'sucsess'


@app.route('/write',methods = ['PUT'])
def write():
    global tree
    path = request.form['path']
    path = format_path(path, 'folder')

    if path not in tree.keys():
        return "Directory doesn't exist"
    if 'file' not in request.files:
        return 'No file received'
    file = request.files['file']

    filename = file.filename
    file.save(filename)
    # TODO: send the command to the servers
    tree[path+filename] = [os.stat(filename).st_size]
    save_tree(tree)

    return 'sucsess'


if __name__ == '__main__':
   app.run(host=sys.argv[1], port=int(sys.argv[2]), debug = True)

