import os
import sys
import socket
import asyncio
import time
import mysql.connector


server_name = ''
server_port = 4242
user_num = 1024
frame_size = 1024
timer = 10**6


if __name__ != '__main__':
    exit('Wrong start point')


if len(sys.argv) not in [2,3]:
    exit('Wrong input parameters')


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((server_name, server_port))


for i in range(timer):
    data, client_addr = sock.recvfrom(frame_size)
    data = data.decode('utf-8')
    print(f"Message was reiced from {client_addr} user")
    print(data)

sock.close()

