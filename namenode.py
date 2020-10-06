from flask import Flask, redirect, url_for, request
import sys
import pickle
import os

app = Flask(__name__)

tree = {}

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


if __name__ == '__main__':
   app.run(host=sys.argv[1], port=int(sys.argv[2]), debug = True)

