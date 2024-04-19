import datetime
from aioquic.quic.events import QuicEvent, StreamDataReceived, ConnectionTerminated
import json
import struct

class TYPE:
    #user conditions
    SIG = "SIG" #sing up
    CON = "CON" #control of chats
    PUS = "SEN" #client sands message
    PUL = "PUL" #client gets chat updates

    #server conditions
    ACK = "ACK" #acknowledgement
    DEN = "DEN" #denay of servise
    CHT = "CHT" #server sands chat
    SEN = "UPD" #server sands messages

    DFT = "DFT" #default

    type_list = ["SIG", "CON", "SEN", "PUL", "ACK",
                 "DEN", "CHT", "UPD", "DFT"]


class Frame():
    struct  = ["type", "time"]
    type    = TYPE.DFT
    event   = 0
    mess    = 0
    time    = 0
    valid   = 1

    def __init__(self, event = 0):
        try:
            if event:
                self.event= event 
                self.mess = json.loads(event.data[2:].decode('utf-8'))
                self.type = self.mess['type']
                self.time = self.mess['time']
            else:
                self.time = datetime.datetime.now().strftime(' %H:%M:%S')
        except Exception:
            self.valid = -1


    def from_json(self):
        if self.type == TYPE.DFT:
            return self
        if self.type == TYPE.SIG:
            return Sig(self.event)
        if self.type == TYPE.ACK:
            return Ack(self.event)
        if self.type == TYPE.DEN:
            return Den(self.event)


    def to_json(self):
        frame = json.dumps({
                "type": self.type,
                "time": self.time,
                }).encode("utf-8")
        return struct.pack("!H", len(frame))+frame

    
    def __str__(self) -> str:
        return f"time: {self.time}\t\tJSN: {self.type}"


class Sig(Frame):
    struct   = ["type", "time", "name", "password"]
    name     = ''
    password = ''

    def __init__(self, event=0, name = '', password = ''):
        super().__init__(event)
        self.type = TYPE.SIG
        try:
            if event:
                self.name     = self.mess['name']
                self.password = self.mess['password']
            else:
                self.name     = name
                self.password = password 
        except Exception:
            self.valid = -1

    def to_json(self):
        frame = json.dumps({
                "type": self.type,
                "time": self.time,
                "name": self.name,
                "password": self.password,
                }).encode("utf-8")
        return struct.pack("!H", len(frame))+frame

    
    def __str__(self) -> str:
        return f"time:{self.time}\t\tJSN: {self.type} name:{self.name} pass:{self.password}"
    

class Ack(Frame):
    def __init__(self, event=0):
        super().__init__(event)
        self.type = TYPE.ACK


class Den(Frame):
    def __init__(self, event=0):
        super().__init__(event)
        self.type = TYPE.DEN


    



        

