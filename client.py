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
def main():
    print('Welcome Client!')
    print('what do you want to do?')
    print('Your options are:')
    print('''''')