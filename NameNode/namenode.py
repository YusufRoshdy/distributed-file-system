import os
import pickle
import sys
import io

import requests
from flask import Flask, redirect, request, send_file, url_for, Response, abort, jsonify

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
    ip = request.remote_addr
    port = request.form['port']
    
    res = '' # Response()

    print('\n', ip,':', port, 'requested to join\n')
    if (ip, port) not in [(x['ip'], x['port']) for x in pool]:
        pool.append({'ip': ip, 'port': port, 'initialized':False})
        print(ip,':', port, 'has joind the cluster')
        
        if len(pool) > 1 and pool[0]['initialized']:
            res = get_all_files(pool[0])
        pool[-1]['initialized'] = True
        save_pool(pool)
    else:
        print(ip,':', port, 'already in the cluster')
    # TODO: initialize the server and send all files and folders
    return res # Response(files={})

@app.route('/get_pool', methods=['GET'])
def get_pool():
    global pool
    pool = update_pool(pool)
    return jsonify(pool)

@app.route('/initialize',methods = ['POST'])
def initialize():
    tree = {'./': 1}
    send_command('rm -r *')
    save_tree(tree)
    return 'sucsess'

@app.route('/ls',methods = ['GET'])
def ls():
    path = request.form['path']
    path = format_path(path, 'folder')

    ret = []
    if path not in tree.keys():
        abort(Response(f'{path} is not a directory', status=400))
    for t in tree:
        if path in t and len(path) != len(t):
            if (t[len(path):][-1] == '/' and '/' not in t[len(path):-1]) or '/' not in t[len(path):]:
                ret.append(t[len(path):])
    return jsonify(ret)

@app.route('/info',methods = ['GET'])
def info():
    path = request.form['path']
    folder = format_path(path, 'folder')
    file = format_path(path, 'file')
    if file in tree.keys():
        return jsonify(tree[file])
    elif folder in tree.keys():
        return jsonify(tree[folder])
    else:
        abort(Response(f"{path} is not a file or directory", status=400))
    return NO_CONTENT

@app.route('/mkdir',methods = ['PUT'])
def mkdir():
    global tree
    path = request.form['path']
    
    path = format_path(path, 'folder')
    print(path)
    print(get_parent(path))

    if path in tree.keys():
        abort(Response(f'{path} already exist', status=400))
    
    if not check_parent_exist(path, tree):
        abort(Response(f"Parent directory doesn't exist:", get_parent(path), status=400))

    replicas = send_command('mkdir '+ path)
    if replicas < 1:
        abort(Response(f"The cluster in unavailable", status=400))
    tree[path] = {'replicas': replicas}
    save_tree(tree)
    return NO_CONTENT

@app.route('/touch',methods = ['PUT'])
def touch():
    global tree
    path = request.form['path']

    path = format_path(path, 'file')

    if path in tree.keys():
        abort(Response(f"{path} already exist", status=400))

    print(path)
    print(get_parent(path[2:]))
    if not check_parent_exist(path, tree):
        abort(Response(f"Parent directory doesn't exist", status=400))
    
    # TODO: send the command to the servers and edit tree[path] = [??]
    replicas = send_command('touch '+ path[2:])
    if replicas < 1:
        abort(Response(f"The cluster in unavailable", status=400))
    tree[path] = {"size": 0, 'replicas': replicas} # [size, # of servers] change 1 to be the number of servers
    save_tree(tree)
    return NO_CONTENT

@app.route('/put',methods = ['PUT'])
def put():
    global tree
    global pool
    path = request.form['path']
    path = format_path(path, 'file')
    print(path)
    if not check_parent_exist(path, tree):
        abort(Response(f"Parent directory doesn't exist", status=400))

    print(type(request.form['file']))
    # TODO: send to all servers
    pool = update_pool(pool)
    if len(pool) < 1:
        abort(Response(f'The cluster in unavailable', status=400))

    for server in pool:
        r = requests.post(f'http://{server["ip"]}:{server["port"]}/files/{path[2:]}', 
                        data=request.form['file'])
        if not r.ok:
            abort(Response(r.text, status=400))

    tree[path] = {"size": len(request.form['file']), 'replicas': len(pool)} # [size, # of servers] change 1 to be the number of servers
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
        abort(Response('The cluster is unavailable', status=500))
    
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
        abort(Response(f"{path} doesn't exist", status=400))

    # TODO: send the command to the servers
    replicas = send_command('rm '+ path[2:])
    if replicas < 1:
        abort(Response(f'The cluster in unavailable', status=400))

    tree.pop(path, None)
    save_tree(tree)

    return NO_CONTENT

@app.route('/rmdir',methods = ['DELETE'])
def rmdir():
    global tree
    path = request.form['path']
    force = ''
    if 'force' in request.form:
        force = request.form['force']
    path = format_path(path, 'folder')

    if path not in tree.keys():
        abort(Response(f'{path} is not a directory', status=404))
    files_inside_dir = []
    for t in tree:
        if path in t and len(path) != len(t):
            if force.lower() == 'force':
                files_inside_dir.append(t)
            else:
                abort(Response("Directory is not empty", status=400))
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
        abort(Response(f"{src} doesn't exist", status=400))

    if not check_parent_exist(dest, tree):
        abort(Response(f"Destnation file parent directory doesn't exist", status=400))

    
    replicas = send_command('cp ' + src[2:] + ' ' + dest[2:])
    if replicas < 1:
        abort(Response(f'The cluster in unavailable', status=400))

    tree[dest] = tree[src].copy()
    save_tree(tree)

    return NO_CONTENT

@app.route('/mv',methods = ['PUT'])
def mv():
    global tree
    src = request.form['src']
    dest = request.form['dest']
    src = format_path(src, path_type='file')
    dest = format_path(dest, path_type='file')
    
    if src not in tree.keys():
        abort(Response(f"{src} doesn't exist", status=400))

    if not check_parent_exist(dest, tree):
        abort(Response(f"Destnation file parent directory doesn't exist", status=400))


    replicas = send_command('mv ' + src[2:] + ' ' + dest[2:])
    if replicas < 1:
        abort(Response(f'The cluster in unavailable', status=400)) 
    tree[dest] = tree[src].copy()
    tree.pop(src, None)
    save_tree(tree)

    return NO_CONTENT

if __name__ == '__main__':
   app.run(host=sys.argv[1], port=int(sys.argv[2]), debug = True)

