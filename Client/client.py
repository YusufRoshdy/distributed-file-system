import requests
cur_dir=''
def initialze(html):


    payload = {'key1': 'initialze'}
    r=requests.post(html,data=payload)
    return r
def file_create(html, X, cur_dir):
    ip = html + '/'+'mkfile'

    payload = {'path': cur_dir, 'file': X[1]}
    r = requests.post(ip, data=payload)


def file_read(html, X, cur_dir):
    ip = html + '/'+ 'cat'
    path = cur_dir + '/' + X[1]
    payload = {'path': path}
    r1 = requests.get(ip, params=payload)
    return r1.files

# this file write i dont know
def file_write(html):

    file = input().lower()
    file1=open(file)
    payload = {'key1': 'file_write', 'key2': [file, file1]}
    r1 = requests.put(html, data=payload)

def file_delete(html, X, cur_dir):
    ip = html + '/' + 'rm'
    path = cur_dir + '/' + X[1]
    payload = {'path': path}
    r1 = requests.delete(ip, data=payload)
    return cur_dir
def file_info(html):
    print('Enter the name if the file you want to get the information about:')
    file = input().lower()
    payload = {'key1': 'file_info', 'key2': file}
    r1 = requests.get(html, data=payload)
    return r1.content
def file_copy(html):
    print('Enter the name if the file you want to create the copy of:')
    file = input().lower()
    payload = {'key1': 'file_copy', 'key2': file}
    r1 = requests.post(html, data=payload)

def file_move(html):
    print('Enter the name of the file you want to move:')
    file = input().lower()
    print('Enter the path seperated by "/" where you want to put the file:')
    path = input().lower()
    payload = {'key1': 'file_move', 'key2': [file,path]}
    r=requests.patch(html, data=payload)
def open_directory(html,X, cur_dir):
    ip = html + '/' + 'ls'
    path = cur_dir + '/' + X[1]
    payload = {'path': path}
    r = requests.post(ip, data=payload)
    if(r.content=='empty'):
        print('this directory does not exist')

def read_directory(html,X, cur_dir):
    dir=''
    if(X.len>1):
        dir = X[1]
    ip=html + '/ls'
    path= cur_dir + '/' + dir
    dir= input().lower
    payload = {'path': path}
    r=requests.get(html, data=payload)
    return dir
def make_directory(html, X, cur_dir):

    ip  = html + '/' + 'mkdir'
    path = cur_dir + '/' + X[1]
    payload = {'path': 'make_directory'}
    r = requests.post(ip, data=payload)


def delete_directory(html):
    print('Enter the name of the directory to delete:')
    dir = input().lower()
    payload = {'key1': 'delete_directory', 'key2': dir}
    r=requests.get(html, data=payload)

    if(r.content=='available'):
        print('There are other files in this directory, are you sure you want to delete them? (yes/no)')
        x=input().lower()
        if(x=='yes'):
            payload = {'key1': 'delete_directory_yes', 'key2': dir}
            r=requests.delete(html, data=payload)
        else:
            pass
def get_input(html, X, cur_dir):

    if(X == 'initialze'):
        cur_dir=initialze(html, X, cur_dir)

    if(X== 'file create'):
        file_create(html)
    if (X == 'file read'):
        print(file_read(html))
    if(X=='file write'):
        file_write(html)

    if (X == 'file delete'):
        file_delete(html)
    if (X == 'file info'):
        file_info(html)
    if (X == 'file copy'):
        file_copy(html)
    if (X == 'file move'):
        file_move(html)
    if (X == 'ls'):
        open_directory(html)
    if (X == 'ls'):

        cur_dir = read_directory(html, X, cur_dir)
    if (X == 'make directory'):
        make_directory(html)
    if (X == 'delete directory'):
        delete_directory(html)
    return cur_dir

def main(cur_dir, ip):
     X=input()
     X.split()
     get_input(ip, X, cur_dir)