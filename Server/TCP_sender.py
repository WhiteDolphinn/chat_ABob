from socket import *
import os
import sys
from time import sleep


if __name__ != "__main__":
    exit()

if len(sys.argv) != 4:
    exit()

server_name = sys.argv[1]
server_port = sys.argv[2]
shmem       = sys.argv[3]


print(server_name, server_port)
TCP_Socket = socket(AF_INET, SOCK_STREAM)


TCP_Socket.connect((server_name, server_port))

TCP_Socket.close()


