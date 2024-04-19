import datetime
from aioquic.quic.events import QuicEvent, StreamDataReceived, ConnectionTerminated
import json
import struct

class TYPE:
    #user conditions
    SIG = "SIG" #sing up
    LOG = "LOG" #log in
    CON = "CON" #control of chats
    PUS = "SEN" #client sands message
    PUL = "PUL" #client gets chat updates

    #server conditions
    ACK = "ACK" #acknowledgement
    DEN = "DEN" #denay of servise
    CHT = "CHT" #server sands chat
    SEN = "UPD" #server sands messages

    DFT = "DFT" #default

    type_list = ["SIG", "LOG", "CON", "SEN", "PUL",
                 "ACK", "DEN", "CHT", "UPD", "DFT"]


class Frame():
    mess = 0
    type = TYPE.DFT
    time = -1
    valid = 1
    struct = ["type", "time"]

    def __init__(self, event = 0):
        try:
            if event:
                self.mess = json.loads(event.data.decode('utf-8'))
                self.type = self.mess['type']
                self.time = self.mess['time']
            else:
                self.time = datetime.datetime.now().strftime(' %H:%M:%S')
        except Exception:
            self.valid = -1

    def from_json(self):
        if self.type == TYPE.DFT:
            return self

    def to_json(self):
        frame = json.dumps({
                "type": self.type,
                "time": self.time,
                }).encode("utf-8")
        return struct.pack("!H", len(frame))+frame

    
    def __str__(self) -> str:
        return f"time: {self.time}\t\tJSN: {self.type}"



            


# class sig(json_):
#     struct = ["type", "time", "name", "password"]
#     type = TYPE.SIG
#     name = ''
#     password = ''

#     def __init__(self, mess=0):
#         if mess:
#             self.name = mess['name']
#             self.password = mess['password']
    
#     def set(self, name, password):
#         self.name = name
#         self.password = password

    



        

