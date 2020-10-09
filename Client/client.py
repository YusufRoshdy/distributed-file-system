import requests
cur_dir=''

def initialze(html, X, cur_dir):

    ip = html + 'initialze'
    payload = {'key1': 'initialze'}
    r=requests.post(ip)
    print('initialzed')
    return cur_dir

#here the input is like "mkf file.txt"
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
    return cur_dir

#here the input is like "cat file.txt"
def file_read(html, X, cur_dir):
    ip = html + 'cat'
    path = cur_dir + '/' + X[1]
    print(path)
    payload = {'path': path}
    r1 = requests.get(ip, params=payload)
    #open(X[1], 'wb').write(r1.content)
    print('read complete')
    return r1, cur_dir

# the input is like fw file.txt
def file_write(html, X, cur_dir):

    ip = html + 'fw'
    if (X[1][0] != '/'): X[1] = '/' + X[1]
    path = cur_dir
    #file1=open(X[1])
    file1=X[1]
    payload = {'path':[path,file1]}
    r1 = requests.put(html, data=payload)
    print('wrote')
    return cur_dir
#here the input is like "rm file.txt"

def file_delete(html, X, cur_dir):
    ip = html + 'rm'
    if (X[1][0] != '/'): X[1] = '/' + X[1]
    path = cur_dir + X[1]
    payload = {'path': path}
    r1 = requests.delete(ip, data=payload)
    print('deleted')
    return cur_dir

#not sure tozhe
def file_info(html, X, cur_dir):
    ip = html + 'info'
    if (X[1][0] != '/'): X[1] = '/' + X[1]
    path = cur_dir + X[1]
    payload = {'key1': path,}
    r1 = requests.get(ip, data=payload)
    print('infoed')
    #print(str(r1.content))
    return cur_dir

# here the input is like "fcp file.txt"
def file_copy(html, X, cur_dir):
    if (X[1][0] != '/'): X[1] = '/' + X[1]
    path = cur_dir + X[1]
    ip = html + 'fcp'
    payload = {'path': path}
    r1 = requests.post(ip, data=payload)
    print('copied')
    return cur_dir

# here the input is like "fm file.txt directory"
def file_move(html, X, cur_dir):

    ip = html + 'fm'
    if (X[1][0] != '/'): X[1] = '/' + X[1]
    path = cur_dir + X[1]
    dir = ''
    if (X[2][0] != '/'):
        dir = '/' + X[2]
    else:
        dir = X[2]
    payload = {'path': [path, dir]}
    r=requests.patch(ip, data=payload)

    print('moved')
    return cur_dir

#here the input is like "cd directory"
def open_directory(html,X, cur_dir):
    ip = html + 'ls'
    if(X[1][0]!='/'): X[1]='/'+X[1]
    path = cur_dir + X[1]
    payload = {'path': path}
    r = requests.post(ip, data=payload)
    if(r.content=='empty'):
        print('this directory does not exist')
    print('changed directory')
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
    return dir

#here the input is like "mkdir directory"
def make_directory(html, X, cur_dir):

    ip  = html +  'mkdir'
    if (X[1][0] != '/'): X[1] = '/' + X[1]
    path = cur_dir + X[1]
    payload = {'path': path}
    r = requests.put(ip, data=payload)
    print('made directory')
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

    if(X[0] == 'initialize'):
        cur_dir=initialze(html, X, cur_dir)

    if(X[0]== 'touch'):
        cur_dir=file_create(html, X, cur_dir)
    if (X[0] == 'cat'):
        cur_dir=file_read(html, X, cur_dir)[1]
    if(X[0]=='fw'):
        cur_dir = file_write(html, X, cur_dir)

    if (X[0] == 'rm'):
        cur_dir =file_delete(html, X, cur_dir)
    if (X[0] == 'info'):
        cur_dir =file_info(html, X, cur_dir)
    if (X[0] == 'fcp'):
        cur_dir =file_copy(html, X, cur_dir)
    if (X[0] == 'fm'):
        cur_dir =file_move(html, X, cur_dir)
    if (X[0] == 'cd'):
        cur_dir =open_directory(html, X, cur_dir)
    if (X[0] == 'ls'):

        cur_dir = read_directory(html, X, cur_dir)
    if (X[0] == 'mkdir'):
        cur_dir =make_directory(html, X, cur_dir)
    if (X[0] == 'rmdir'):
        cur_dir =delete_directory(html, X, cur_dir)
    return cur_dir

def main(cur_dir, ip):
     X=input()
     X=X.split(" ")
     print(X)
     cur_dir=get_input(ip, X, cur_dir)
     print(cur_dir)
main('.','http://localhost:23/')