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

    
def main():
    print('Welcome Client!')
    print('what do you want to do?')
    print('Your options are:')
    print('''''')