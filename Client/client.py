import requests
from pathlib import PurePosixPath
from argparse import ArgumentParser
import os


def sizeof_fmt(num: int):
    for unit in ['', 'Ki', 'Mi', 'Gi']:
        if abs(num) < 1024.0:
            break
        num /= 1024.0
    return f"{num:3.1f} {unit}B"


class Client:
    def __init__(self, url: str):
        self.cwd = PurePosixPath('/')
        self.url = url

    def initialize(self, cmd=None):
        '''Clears all files.               Usage: initialize'''
        r = requests.post(f'{self.url}/initialize')
        if not r.ok:
            print('An error occured:', r.text)
            return
        self.cwd = PurePosixPath('/')
        print('Initialized')

    #here the input is like "touch file.txt"
    def touch(self, cmd):
        '''Creates new file                Usage: touch <file path>'''
        if len(cmd) < 2:
            print('File name is required')
            return
        filename = cmd[1]
        path = str(self.cwd / filename)
        r = requests.put(f'{self.url}/touch', data={'path': path})
        if not r.ok:
            print('An error occured:', r.text)
            return

    #here the input is like "get file.txt"
    def get(self, cmd):
        '''Download a file.                Usage: get <filename> <destination>'''
        filename, dest = cmd[1:]
        path = str(self.cwd / filename)

        if not os.path.exists(PurePosixPath(dest).parent):
            print("Destination parent directory doesn't exist")
            return

        r = requests.get(f'{self.url}/get', data={'path': path})
        if not r.ok:
            print(r.text)
            return

        with open(dest, "wb") as fp:
            fp.write(r.content)

    # the input is like put file.txt dir/name.txt
    def put(self, cmd):
        '''Upload a file.                  Usage: put <file path> <destination path>'''
        filename, dest = cmd[1:]
        if not os.path.exists(filename):
            print(filename, "doesn't exist")
            return 
        content = open(filename).read()
        path = str(self.cwd / dest)

        r = requests.put(f'{self.url}/put',
                        data={'path': path, 'file': content})
        if not r.ok:
            print('An error occured:', r.text)
            return

    #here the input is like "rm file.txt"
    def rm(self, cmd):
        '''Remove a file.                  Usage: rm <file path>'''
        filename = cmd[1]
        if filename[0] != '/':
            filename = '/' + filename

        path = str(self.cwd / filename)
        r = requests.delete(f'{self.url}/rm', data={'path': path})
        if not r.ok:
            print('An error occured:', r.text)
            return

    def info(self, cmd):
        '''Get info about file.            Usage: info <file path>'''
        filename = cmd[1]
        if filename[0] != '/':
            filename = '/' + filename
        path = str(self.cwd / filename)
        r = requests.get(f'{self.url}/info', data={'path': path})
        if not r.ok:
            print('An error occured:', r.text)
            return
        
        if 'size' in r.json().keys():
            print('size: ', sizeof_fmt(r.json()['size']))
        if 'replicas' in r.json().keys():
            print('replicas: ', r.json()['replicas'])

    def pool(self, cmd=None):
        '''Lists available servers.        Usage: pool'''
        r = requests.get(f'{self.url}/get_pool')
        for idx, server in enumerate(r.json(),1):
            print(f'Server {idx}:', 'ip',server['ip'], ', port', server['port'], ', initialized', server['initialized'])

    # here the input is like "cp file.txt dir"
    def cp(self, cmd):
        '''Copy a file.                    Usage: cp <src> <dest>'''
        if len(cmd) < 3:
            print('Both file name and destination are required')
            return

        filename, dest = cmd[1:]
        if filename[0] != '/':
            filename = '/' + filename

        if dest[0] != '/':
            dest = '/' + dest

        payload = {'src': str(self.cwd / filename), 'dest': str(self.cwd / dest)}
        r = requests.post(f'{self.url}/cp', data=payload)
        if not r.ok:
            print('An error occured:', r.text)
            return

    # here the input is like "mv file.txt directory"
    def mv(self, cmd):
        '''Moves (or renames) a file.      Usage: mv <src> <dest>'''
        filename, dest = cmd[1:]
        if filename[0] != '/':
            filename = '/' + filename

        path = str(self.cwd / filename)

        if dest[0] != '/':
            dest = str(self.cwd / dest)

        payload = {'src': path, 'dest': dest}
        r = requests.put(f'{self.url}/mv', data=payload)
        if not r.ok:
            print('An error occured:', r.text)
            return
        
    #here the input is like "cd directory"
    def cd(self, cmd):
        '''Changes the current directory.  Usage: cd <directory>'''
        directory = cmd[1]
        parts = directory.split('/')
        while parts[0] == '..':
            self.cwd = self.cwd.parent
            parts = parts[1:]
            if len(parts) == 0:
                return

        directory = PurePosixPath('/'.join(parts))

        if not directory.is_absolute():
            directory = self.cwd / directory

        payload = {'path': str(directory)}
        r = requests.get(f'{self.url}/ls', data=payload)
        if not r.ok:
            print(r.text)
            return

        # If request passed, the folder exists
        self.cwd = directory

    #here the input is like "ls directory"
    def ls(self, cmd):
        '''Lists directory contents.       Usage: ls [directory]'''
        directory = self.cwd
        if len(cmd) > 1:
            directory = PurePosixPath(cmd[1])

        if not directory.is_absolute():
            directory = self.cwd / directory

        r = requests.get(f'{self.url}/ls', data={'path': str(directory)})
        print(*r.json(), sep='\n')

    #here the input is like "mkdir directory"
    def mkdir(self, cmd):
        '''Create an empty directory.      Usage: mkdir <directory>'''
        directory = PurePosixPath(cmd[1])
        if not directory.is_absolute():
            directory = self.cwd / directory
        r = requests.put(f'{self.url}/mkdir', data={'path': str(directory)})
        if not r.ok:
            print(r.text)
            return

    def rmdir(self, cmd):
        '''Remove a directory.             Usage: rmdir <directory>'''
        directory = PurePosixPath(cmd[1])
        if not directory.is_absolute():
            directory = self.cwd / directory

        r = requests.delete(f'{self.url}/rmdir', data={'path': str(directory)})
        if not r.ok:
            print(r.text)
            if r.status_code == 400:
                answer = ''
                while answer not in ['y', 'n']:
                    print("Do you still want to delete? (y/n)")
                    answer = input()
                if answer == 'y':
                    payload = {'path': str(directory), 'force': 'force'}
                    r = requests.delete(f'{self.url}/rmdir', data=payload)

    def exit(self, cmd=None):
        '''Exits.                          Usage: exit'''
        pass


def main():
    parser = ArgumentParser()
    parser.add_argument("ip", help="The IP of the naming server")
    parser.add_argument("-p", "--port", default=5000, type=int, help="The port of the naming server")
    args = parser.parse_args()
    ip = args.ip
    port = args.port
    address = f'{ip}:{port}'

    client = Client(address)
    available_commands = [attr for attr in dir(client) if not attr.startswith('_') and callable(getattr(client, attr))]
    cmd = ''
    def print_help():
        for command in available_commands:
            print(f'{command:25} - ', getattr(client, command).__doc__)

    while True:
        print(f'{client.cwd}> ', end='')
        cmd = input().split(' ')
        if cmd[0] == 'exit':
            break
        if cmd[0] == 'help':
            print_help()
            continue
        if cmd[0] not in available_commands:
            print('Unkown command. Available commands:\n')
            print_help()
            continue
        func = getattr(client, cmd[0])
        func(cmd)

if __name__ == '__main__':
    main()