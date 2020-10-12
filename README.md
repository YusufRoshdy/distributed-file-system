# Distributed File System

This project is a *Distributed File System (DFS)*, which will be hosted on AWS. It is the final project for *Introduction to Distributed System* course at Innopolis University. The goal of the project is to have a robust and fault-tolerant distributed file system, even if some server failed the system stays up.

Team members:
- Shamil Khastiev(Storage)
- Utkarsh Kalra(Clint, Ui)
- Yusuf Mesbah(Storage, Client, NameNode)

 [GitHub link](https://github.com/YusufRoshdy/distributed-file-system)
 DockerHub links:
 [dfs_server](https://hub.docker.com/r/yusufmesbah/dfs_server)
 [dfs_namenode](https://hub.docker.com/r/yusufmesbah/dfs_namenode)
 [dfs_client](https://hub.docker.com/r/yusufmesbah/dfs_client)


## Architecture

![](https://i.imgur.com/KpEiTc1.png)
###### Nodes are communicating using REST API

### Storage Servers
The storage servers will run on a docker image hosted on AWS EC2 machines and will be connected with a VPC with there namenode.
The storage serves will have the actual data of the DFS.
They start by sending a connection request to the namenode to join the cluster and then they start listening to the commands coming from the name node.

### NameNode
The namenode is a server that does special tasks:
- Only store metadata about the DFS
- Validate the clients' commands before relaying them to the servers
- Manage the new servers that join the cluster and sync them

### Clients
The clients can be run from anywhere to connect to the namenode and start sending the user requests to the DFS.

## How to Run

### Storage Servers
To run the a storage server you can run it directly on Unix based os or using the dfs_server docker image
#### Run Directly
`python3 server.py <port to run on> <namenode address>`
#### Run Docker image
`docker run --rm -p <server port>:<server port> dfs_server <server port> <namenode address>`

### Namenode
To run the The namenode you can run it directly or using the dfs_namenode docker image
#### Run Directly
`python3 namenode.py <port to run on>`
#### Run Docker image
`docker run --rm  dfs_namenode <Namenode port>`

### Clients
To run a client you can run it directly, using the dfs_client docker image or Using the Client user interface program.
#### Run Directly
`python3 client.py [-h] [-p namenode PORT] <namenode ip>`
#### Run Docker image
`docker run --rm -it dfs_client [-h] [-p namenode PORT] <namenode ip>`

#### CLI Usage
| Command    |  Description                    | Usage                                |
|------------|---------------------------------|--------------------------------------|
| cd         |  Changes the current directory. | `cd <directory>`                     |
| cp         |  Copy a file.                   | `cp <src> <dest>`                    |
| exit       |  Exits.                         | `exit`                               |
| get        |  Download a file.               | `get <filename> <destination>`       |
| info       |  Get info about file.           | `info <file path>`                   |
| initialize |  Clears all files.              | `initialize`                         |
| ls         |  Lists directory contents.      | `ls [directory]`                     |
| mkdir      |  Create an empty directory.     | `mkdir <directory>`                  |
| mv         |  Moves (or renames) a file.     | `mv <src> <dest>`                    |
| pool       |  Lists available servers.       | `pool`                               |
| put        |  Upload a file.                 | `put <file path> <destination path>` |
| rm         |  Remove a file.                 | `rm <file path>`                     |
| rmdir      |  Remove a directory.            | `rmdir <directory>`                  |
| touch      |  Creates new file               | `touch <file path>`                  |


### Graphical User interface
In the GUI, first, the namenode address is required and after pressing start you can choose a command from the dropdown menu and give the arguments to the command, after pressing submit the client will send the request and when it receives a response, it will display the output in the corresponding dialogue
![](https://i.imgur.com/OlRDxhc.jpg)
![](https://i.imgur.com/RW2E0UP.jpg)
![](https://i.imgur.com/umcW1Kb.jpg)