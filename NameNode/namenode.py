import os
import pickle
import sys
import io

import requests
from flask import Flask, redirect, request, send_file, url_for, Response

from util import *

NO_CONTENT = ('', 204)

app = Flask(__name__)

tree = load_tree()
pool = load_pool()
pool = update_pool(pool)

def get_all_files(server):
    r = requests.get(f'http://{server["ip"]}:{server["port"]}/send_zip/')
    return r.content # Response(files={'file': io.BytesIO(r.content)})

def send_command(command):
    global pool
    print('sending command:', command, flush=True)
    print('pool size', len(pool))
    pool = update_pool(pool)
    for server in pool:
        r = requests.post(f'http://{server["ip"]}:{server["port"]}/command/', data=command)
    return len(pool)

@app.route('/connect', methods=['POST'])
def connect():
    global pool
    ip = request.form['ip']
    port = request.form['port']

    print('\n', ip,':', port, 'requested to join\n')
    if {'ip': ip, 'port': port} not in pool:
        pool.append({'ip': ip, 'port': port})
        print(ip,':', port, 'has joind the cluster')
        save_pool(pool)
    # TODO: initialize the server and send all files and folders
    res = '' # Response()
    if len(pool) > 1:
        res = get_all_files(pool[0])
    return res # Response(files={})

@app.route('/get_pool', methods=['GET'])
def get_pool():
    global pool
    pool = update_pool(pool)
    if len(pool) == 0:
        return 'Pool is empty'
    return '\n'.join([str(x) for x in pool])

@app.route('/initialize',methods = ['POST'])
def initialize():
    tree = tree = {'./': 1}
    # TODO: send the command to the servers
    save_tree(tree)
    return 'sucsess'

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

@app.route('/info',methods = ['GET'])
def info():
    path = request.form['path']
    folder = format_path(path, 'folder')
    file = format_path(path, 'file')
    if file in tree.keys():
        return '\n'.join([str(x) for x in tree[file]])
    elif folder in tree.keys():
        return str(tree[folder])
    else:
        return path + ' is not a file or directory'

@app.route('/mkdir',methods = ['PUT'])
def mkdir():
    global tree
    path = request.form['path']
    
    path = format_path(path, 'folder')

    if path in tree.keys():
        return path + ' already exist'
    
    if not check_parent_exist(path, tree):
        return "Parent directory doesn't exist"

    replicas = send_command('mkdir '+ path[2:-1])
    if replicas < 1:
        return 'The cluster in unavailable'
    tree[path] = replicas
    save_tree(tree)
    return 'success'

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
    replicas = send_command('touch '+ path[2:])
    if replicas < 1:
        return 'The cluster in unavailable'
    tree[path] = [0, replicas] # [size, # of servers] change 1 to be the number of servers
    save_tree(tree)
    print('hi')
    return 'sucsess'

@app.route('/put',methods = ['PUT'])
def put():
    global tree
    global pool
    path = request.form['path']
    path = format_path(path, 'file')
    if not check_parent_exist(path, tree):
        return "Parent directory don't exist"

    print(type(request.form['file']))
    # TODO: send to all servers
    pool = update_pool(pool)
    if len(pool) < 1:
        return 'The cluster in unavailable'
    for server in pool:
        requests.post(f'http://{server["ip"]}:{server["port"]}/files/{path[2:]}', 
                        data=request.form['file'])

    tree[path] = [1, len(request.form['file'])] # [size, # of servers] change 1 to be the number of servers
    save_tree(tree)
    return NO_CONTENT

@app.route('/get',methods = ['GET'])
def get():
    global tree
    global pool
    path = request.form['path']
    path = format_path(path, 'file')

    if path not in tree.keys():
        return path + " doesn't exist"
    # TODO: request from a server that has the file
    pool = update_pool(pool)
    if len(pool) < 1:
        return 'The cluster in unavailable'
    r = requests.get(f"http://{pool[0]['ip']}:{pool[0]['port']}/files/"+path[2:])
    # print(r)
    # print(r.text)
    # print(r.content)

    return r.content

@app.route('/rm',methods = ['DELETE'])
def rm():
    global tree
    path = request.form['path']
    path = format_path(path, 'file')

    if path not in tree.keys():
        return path + " doesn't exist"

    # TODO: send the command to the servers
    replicas = send_command('rm '+ path[2:])
    if replicas < 1:
        return 'The cluster in unavailable'
    tree.pop(path, None)
    save_tree(tree)

    return 'success'

@app.route('/rmdir',methods = ['DELETE'])
def rmdir():
    global tree
    path = request.form['path']
    force = ''
    if 'force' in request.form:
        force = request.form['force']
    path = format_path(path, 'folder')

    if path not in tree.keys():
        return path + " is not a directory"
    files_inside_dir = []
    for t in tree:
        if path in t and len(path) != len(t):
            if force.lower() == 'force':
                files_inside_dir.append(t)
            else:
                return "Directory is not empty"
    replicas = 0
    if force.lower() == 'force':
        replicas = send_command('rm -r ' + path[2:-1])
    else:
        replicas = send_command('rmdir ' + path[2:-1])
    
    if replicas < 1:
        return 'The cluster in unavailable'

    for f in files_inside_dir:
        tree.pop(f, None)
        save_tree(tree)
    tree.pop(path, None)
    save_tree(tree)

    return NO_CONTENT

@app.route('/cp',methods = ['POST'])
def cp():
    global tree
    src = request.form['src']
    dest = request.form['dest']
    src = format_path(src, path_type='file')
    dest = format_path(dest, path_type='file')
    
    if src not in tree.keys():
        return src + " doesn't exist"

    if not check_parent_exist(dest):
        return "destnation file parent directory doesn't exist"

    
    replicas = send_command('cp ' + src[2:] + ' ' + dest[2:])
    if replicas < 1:
        return 'The cluster in unavailable'
    tree[dest] = tree[src]
    save_tree(tree)

    return 'success'

@app.route('/mv',methods = ['PUT'])
def mv():
    global tree
    src = request.form['src']
    dest = request.form['dest']
    src = format_path(src, path_type='file')
    dest = format_path(dest, path_type='file')
    
    if src not in tree.keys():
        return src + " doesn't exist"

    if not check_parent_exist(dest):
        return "destnation file parent directory doesn't exist"


    replicas = send_command('mv ' + src[2:] + ' ' + dest[2:])
    if replicas < 1:
        return 'The cluster in unavailable'  
    tree[dest] = tree[src]
    tree.pop(src, None)
    save_tree(tree)

    return 'sucsess'

if __name__ == '__main__':
   app.run(host=sys.argv[1], port=int(sys.argv[2]), debug = True)

