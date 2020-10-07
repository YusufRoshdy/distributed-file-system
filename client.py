import requests
def initialze(html):
    
    
    payload = {'key1': 'initialze'}
    r=requests.post(html,data=payload)
    return r
def file_create(html):
    print('Enter the file name you want to create:')
    file=input().lower()
    payload = {'key1': 'file_create', 'key2': file}
    r = requests.post(html, data=payload)
    return r

 def file_read(html):
    print('Enter the file name you want to read:')
    file = input().lower()
    payload = {'key1': 'file_read', 'key2': file}

    r1 = requests.get(html, params=payload)
    return r1.content
def file_write(html):
    print('Enter the file name you want to write to dfs(should be in the same folder):')
    file = input().lower()
    file1=open(file)
    payload = {'key1': 'file_write', 'key2': [file, file1]}
    r1 = requests.put(html, data=payload)
def file_delete(html):
    print('Enter the name of the file you want to delete:')
    file = input().lower()
    payload = {'key1': 'file_delete', 'key2': file}
    r1 = requests.delete(html, data=payload)
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
 def open_directory(html):
    print('Enter the name of the directory to open:')
    file = input().lower()

    payload = {'key1': 'open_directory', 'key2': file}
    r = requests.post(html, data=payload)
def read_directory(html):
    print('Enter the name of the directory to read:')
    dir= input().lower
    payload = {'key1': 'read_directory', 'key2':dir}
    r=requests.get(html, data=payload)
    return r.content
def make_directory(html):
    print('Enter the name of the directory to make:')
    dir = input().lower
    payload = {'key1': 'make_directory', 'key2': dir}
    r = requests.post(html, data=payload)

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
def get_input(html, X):

    if(X == 'initialze'):
        initialze(html)
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
    if (X == 'open directory'):
        open_directory(html)
    if (X == 'read directory'):
        read_directory(html)
    if (X == 'make directory'):
        make_directory(html)
    if (X == 'delete directory'):
        delete_directory(html)
               
def main():
    print('Welcome Client!')
    print('what do you want to do?')
    print('Your options are:')
    print('''''')