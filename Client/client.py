import requests
cur_dir=''
from flask import Flask, request, send_from_directory
import re
def initialze(html, X, cur_dir):

    ip = html + 'initialze'

    r=requests.post(ip)
    print('initialzed')
    return cur_dir

#here the input is like "touch file.txt"
def file_create(html, X, cur_dir):
    ip = html +'touch'
    if(len(X)<2):
        print('give the name of the file you want to create')
        return
    if (X[1][0] != '/'): X[1] = '/' + X[1]
    path = cur_dir + X[1]
    payload = {'path': path}
    r = requests.put(ip, data=payload)
    print('file created')
    print(r.text)
    return r.content

#here the input is like "cat file.txt"
def file_read(html, X, cur_dir):
    ip = html + 'get'
    file_name = X[1]
    if (X[1][0] != '/'): X[1] = '/' + X[1]
    path = cur_dir + X[1]
    payload = {'path': path}

    r=requests.get(ip,data=payload)
    with open(file_name, "wb") as fp:
        fp.write(r.content)



    #open(X[1], 'wb').write(r1.content)
    print(r.text)
    print('read complete')
    return r.content

# the input is like put file.txt dir/name.txt
def file_write(html, X, cur_dir):

    ip = html + 'put'
    if (X[2][0] != '/'): X[2] = '/' + X[2]
    path = cur_dir+X[2]
    r = requests.put(ip,
                     data={'path': path, 'file': open(X[1]).read()})

    print(r.text)
    return r.content
#here the input is like "rm file.txt"

def file_delete(html, X, cur_dir):
    ip = html + 'rm'
    if (X[1][0] != '/'): X[1] = '/' + X[1]
    path = cur_dir + X[1]
    payload = {'path': path}
    r1 = requests.delete(ip, data=payload)

    print(r1.text)
    return r1.content

#not sure tozhe
def file_info(html, X, cur_dir):
    ip = html + 'info'
    if (X[1][0] != '/'): X[1] = '/' + X[1]
    path = cur_dir + X[1]
    payload = {'path': path}
    r1 = requests.get(ip, data=payload)

    print(str(r1.text))
    return r1.content


def pool(html):
    ip =html+'get_pool'

    r = requests.get(ip)
    print(r.content)

    return r.content

# here the input is like "cp file.txt dir"
def file_copy(html, X, cur_dir):
    if (X[1][0] != '/'): X[1] = '/' + X[1]
    print(cur_dir,'yfiyf')

    if(len(X)<3):
        print('give the directory to copy in')
        return
    if(X[2][0] != '/'): X[2] = '/' + X[2]
    ip = html + 'cp'
    print(cur_dir+X[1])
    payload = {'src': cur_dir+X[1], 'dest': cur_dir+X[2]}
    r1 = requests.post(ip, data=payload)
    print(r1.text)
    return r1.content

# here the input is like "mv file.txt directory"
def file_move(html, X, cur_dir):

    ip = html + 'mv'
    if (X[1][0] != '/'): X[1] = '/' + X[1]
    path = cur_dir + X[1]
    dir = ''
    if (X[2][0] != '/'):
        dir =cur_dir+ '/' + X[2]
    else:
        dir = cur_dir+X[2]
    payload = {'src':path, 'dest':dir}
    r=requests.put(ip, data=payload)

    print('moved')
    print(r.text)
    return str(r.content)

#here the input is like "cd directory"
def open_directory(html,X, cur_dir):
    ip = html + 'ls'
    path=''
    if(X[1]=='..'):
        dirs = cur_dir.split('/')
        for i in range(len(dirs)-1):
            path = path+dirs[i]+'/'
        path = path[:-1]
        print(path)
        return path
    else:
        if(X[1][0]!='/'): X[1]='/'+X[1]
        path = cur_dir + X[1]
        payload = {'path': path}
        r = requests.get(ip, data=payload)
        things = re.split('[\n /]', r.text)
        X[1] = X[1].split('/')
        print('x1', X[1])
        print('things', things)
        print('r.text', str(r.text))
        #print(str(r.content) + 'sjshshs')
        substring='not a directory'
        if(substring in r.text):

            print('this directory does not exist')
            return cur_dir
        else:
            print('changed')
            print(path)
            return path



#here the input is like "ls directory"
def read_directory(html,X, cur_dir):
    dir=''
    if(len(X)>1):
        if (X[1][0] != '/'): X[1] = '/' + X[1]
        dir = X[1]
    ip=html + 'ls'
    path= cur_dir + '/' + dir

    payload = {'path': path}
    r=requests.get(ip, data=payload)
    print('sent ls')
    print(str(r.text))
    return r.content

#here the input is like "mkdir directory"
def make_directory(html, X, cur_dir):

    ip  = html +  'mkdir'
    if (X[1][0] != '/'): X[1] = '/' + X[1]
    path = cur_dir + X[1]
    payload = {'path': path}
    r = requests.put(ip, data=payload)
    print('made directory')
    print(str(r.content))
    return r.content

#this i am not sure
def delete_directory(html, X, cur_dir):

    ip = html+'rmdir'
    if (X[1][0] != '/'): X[1] = '/' + X[1]
    path = cur_dir + X[1]
    payload = {'path': path }
    r=requests.delete(ip, data=payload)

    if(r.text==path+' is not a directory'):
        print(path+' is not a directory')

    elif(r.text=='Directory is not empty'):
        print(path+' is not empty')
        print("do you still want to delete?(yes/no)")
        check = input()
        if(check=='yes'):
            payload = {'path': path, 'force':'force'}
            r=requests.delete(ip, data = payload)
            print('deleted')
        else:
            print('not deleted, be careful next time you bitch')
    return r.content

def get_input(html, X, cur_dir):

    if(X[0] == 'initialize'):
        cur_dir=initialze(html, X, cur_dir)

    if(X[0]== 'touch'):
        cur_dir=file_create(html, X, cur_dir)
    if (X[0] == 'get'):
        cur_dir=file_read(html, X, cur_dir)
    if(X[0]=='put'):
        cur_dir = file_write(html, X, cur_dir)

    if (X[0] == 'rm'):
        cur_dir =file_delete(html, X, cur_dir)
    if (X[0] == 'info'):
        cur_dir =file_info(html, X, cur_dir)
    if (X[0] == 'cp'):
        cur_dir =file_copy(html, X, cur_dir)
    if (X[0] == 'mv'):
        cur_dir =file_move(html, X, cur_dir)
    if (X[0] == 'cd'):
        cur_dir =open_directory(html, X, cur_dir)
    if (X[0] == 'ls'):

        cur_dir = read_directory(html, X, cur_dir)
    if (X[0] == 'mkdir'):
        cur_dir =make_directory(html, X, cur_dir)
    if (X[0] == 'rmdir'):
        cur_dir =delete_directory(html, X, cur_dir)
    if (X[0] == 'get_pool'):
        cur_dir =pool(html)
    return cur_dir

def main(cur_dir):
    print('Enter the ip to the namemode')
    ip = input()
    print('Enter the port')
    port = input()
    ip = ip + ':' + port +'/'
    while(1):
         X=input()
         X=X.split(" ")
         print(len(X))
         if(X[0]=='cd'):
             cur_dir =get_input(ip, X, cur_dir)
         else:
             get_input(ip, X, cur_dir)

         print(cur_dir)
main('.')