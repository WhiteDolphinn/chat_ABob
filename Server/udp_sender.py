import socket
import os
import time
import sys
import random

user_name       = ''
server_name     = ''
sender_port     = 1111
reciever_port   = 1112
server_port     = 4242


if __name__ != '__main__':
    exit('Wrong start point')


if len(sys.argv) < 4:
    exit('Wrong input parameters')


sender_port = sys.argv[1]
reciever_port = sys.argv[2]
sender_message = ' '.join(sys.argv[3::])


sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender_message = str(reciever_port)+'\n'+sender_message
print(sender_message)
sender_sock.sendto(sender_message.encode('utf-8'), (server_name, server_port))

print("Message was transmited")

sender_sock.close()
