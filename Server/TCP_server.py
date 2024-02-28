import os
import sys
import socket
import asyncio
import datetime
import mysql.connector
import subprocess


class colors:
    RED     = '\033[91m'
    GREEN   = '\033[92m'
    YELLOW  = '\033[93m'
    BLUE    = '\033[94m'
    DEFAULT = '\033[0m'


server_name =   ''
server_port =   4242
user_num    =   1024
frame_size  =   1024
timer       =   10**6
width       =   min (50, os.get_terminal_size()[0])


if __name__ != '__main__':
    exit('Wrong start point')


if len(sys.argv) != 3:
    exit(colors.RED+
         'Wrong input parameters\n'+
         colors.YELLOW+
         'There is a correct stucture:\n'+
         '  -server name (Default = d )\n'+
         '  -server port (Default = d (4242))'+
         colors.DEFAULT)
    


if sys.argv[1] != 'd':
    server_name = sys.argv[1]

if sys.argv[2] != 'd':
    server_port = int(sys.argv[2])


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((server_name, server_port))


subprocess.call("clear", shell = True)

print(colors.YELLOW + "Server is working\n" +
      f"name: {server_name if server_name!='' else 'localhost'}, "+
      f"port: {server_port}"+colors.DEFAULT)


for i in range(timer):
    data, client_addr = sock.recvfrom(frame_size)
    data = data.decode('utf-8')
    print('-'*width)
    print(colors.GREEN + f"Message {i} from {client_addr} at"+
          f"{datetime.datetime.now().strftime(' %H:%M:%S')}" + colors.DEFAULT)
    print(f"{data:{width}}")
    print('-'*width)

sock.close()

