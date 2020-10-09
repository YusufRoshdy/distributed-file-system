import requests
cur_dir=''

def initialze(html, X, cur_dir):

    ip = html + '/' + 'initialze'
    payload = {'key1': 'initialze'}
    r=requests.post(ip)
    return cur_dir

#here the input is like "mkf file.txt"
def file_create(html, X, cur_dir):
    ip = html + '/'+'mkf'

    payload = {'path': cur_dir, 'file': X[1]}
    r = requests.post(ip, data=payload)
    return cur_dir

#here the input is like "cat file.txt"
def file_read(html, X, cur_dir):
    ip = html + '/'+ 'cat'
    path = cur_dir + '/' + X[1]
    payload = {'path': path}
    r1 = requests.get(ip, params=payload)
    return r1.files, cur_dir

# this file write i dont know
def file_write(html):

    file = input().lower()
    file1=open(file)
    payload = {'key1': 'file_write', 'key2': [file, file1]}
    r1 = requests.put(html, data=payload)

#here the input is like "rm file.txt"
def file_delete(html, X, cur_dir):
    ip = html + '/' + 'rm'
    path = cur_dir + '/' + X[1]
    payload = {'path': path}
    r1 = requests.delete(ip, data=payload)
    return cur_dir

#not sure tozhe
def file_info(html):
    print('Enter the name if the file you want to get the information about:')
    file = input().lower()
    payload = {'key1': 'file_info', 'key2': file}
    r1 = requests.get(html, data=payload)
    return r1.content

# here the input is like "fcp file.txt"
def file_copy(html, X, cur_dir):
    path = cur_dir + '/' + X[1]
    ip = html + '/' + 'fcp'
    payload = {'path': path}
    r1 = requests.post(ip, data=payload)
    return cur_dir

# here the input is like "fm file.txt directory"
def file_move(html, X, cur_dir):

    ip = html + '/' + 'fm'
    path = cur_dir + '/' + X[1]
    dir = ''
    if (X[2][1] != '/'):
        dir = '/' + X[2]
    else:
        dir = X[2]
    payload = {'path': [path, dir]}
    r=requests.patch(html, data=payload)
    return cur_dir

#here the input is like "cd directory"
def open_directory(html,X, cur_dir):
    ip = html + '/' + 'ls'
    if(X[1][1]!='/'): X[1]='/'+X[1]
    path = cur_dir + '/' + X[1]
    payload = {'path': path}
    r = requests.post(ip, data=payload)
    if(r.content=='empty'):
        print('this directory does not exist')
    return path

#here the input is like "ls directory"
def read_directory(html,X, cur_dir):
    dir=''
    if(X.len>1):
        if (X[1][1] != '/'): X[1] = '/' + X[1]
        dir = X[1]
    ip=html + '/ls'
    path= cur_dir + '/' + dir
    dir= input().lower
    payload = {'path': path}
    r=requests.get(html, data=payload)
    return dir

#here the input is like "mkdir directory"
def make_directory(html, X, cur_dir):

    ip  = html + '/' + 'mkdir'
    path = cur_dir + '/' + X[1]
    payload = {'path': 'make_directory'}
    r = requests.post(ip, data=payload)
    return cur_dir

#this i am not sure
def delete_directory(html, X, cur_dir):
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

    if(X[0]== 'mkf'):
        cur_dir=file_create(html, X, cur_dir)
    if (X[0] == 'cat'):
        cur_dir=file_read(html, X, cur_dir)[1]
    if(X[0]=='nano'):
        cur_dir = file_write(html, X, cur_dir)

    if (X == 'rmf'):
        cur_dir =file_delete(html, X, cur_dir)
    if (X == 'file info'):
        cur_dir =file_info(html, X, cur_dir)
    if (X == 'fcp'):
        cur_dir =file_copy(html, X, cur_dir)
    if (X == 'fm'):
        cur_dir =file_move(html, X, cur_dir)
    if (X == 'cd'):
        cur_dir =open_directory(html, X, cur_dir)
    if (X == 'ls'):

        cur_dir = read_directory(html, X, cur_dir)
    if (X == 'mkdir'):
        cur_dir =make_directory(html, X, cur_dir)
    if (X == 'rmdir'):
        cur_dir =delete_directory(html, X, cur_dir)
    return cur_dir

def main(cur_dir, ip):
     X=input()
     X.split()
     cur_dir=get_input(ip, X, cur_dir)