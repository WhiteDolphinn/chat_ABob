import datetime
from aioquic.quic.events import QuicEvent, StreamDataReceived, ConnectionTerminated
import json
import struct
from src.user import User
# from src.chatlist import Chat

class TYPE:
    #user conditions
    SIG = "SIG" #sing up
    CON = "CON" #control of chats
    MES = "MES" #client sands message
    PUL = "PUL" #client gets chat updates

    #server conditions
    ACK = "ACK" #acknowledgement
    DEN = "DEN" #denay of servise
    INF = "INF" #server sends userinfo
    CHT = "CHT" #server sands chat
    SEN = "UPD" #server sands messages
    CHI = "CHI" #server sends chatinfo

    DFT = "DFT" #default

    type_list = ["SIG", "CON", "SEN", "PUL", "ACK",
                 "DEN", "CHT", "UPD", "DFT"]
    

class ACTION:
    #actions with chats
    CREAT   = "CREAT"
    DEL     = "DEL"
    BUN     = "BUN"
    ADD     = "ADD"
    DEFAULT = "DEF"
    EXIT    = "EXIT"
    INFO    = "INFO"


class Frame():
    struct  = ["type", "time"]
    type    = TYPE.DFT
    event   = 0
    data    = 0
    mess    = 0
    time    = 0
    valid   = 1

    def __init__(self, event = 0, data = 0):
        try:
            if data:
                self.data = data
                self.mess = json.loads(data[2::])
                self.type = self.mess['type']
                self.time = self.mess['time']
                # event = 1
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
        if self.type == TYPE.SIG:
            return Sig(event = self.event, data = self.data)
        if self.type == TYPE.ACK:
            return Ack(event = self.event, data = self.data)
        if self.type == TYPE.DEN:
            return Den(event = self.event, data = self.data)
        if self.type == TYPE.INF:
            return InfoFrame(event = self.event, data = self.data)
        if self.type == TYPE.CON:
            return ControlFrame(event = self.event, data = self.data)
        if self.type == TYPE.CHI:
            return ChatInfoFrame(event = self.event, data = self.data)
        if self.type == TYPE.MES:
            return MessageFrame(event = self.event, data = self.data)
        if self.type == TYPE.PUL:
            return PullFrame(event = self.event, data = self.data)
        if self.type == TYPE.CHT:
            return ChtFrame(event = self.event, data = self.data)
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


class Sig(Frame):
    struct   = ["type", "time", "name", "password"]
    name     = ''
    password = ''

    def __init__(self, event=0, name = '', password = '', data = 0):
        super().__init__(event=event, data=data)
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
    def __init__(self, event=0, data=0):
        super().__init__(event=event, data=data)
        self.type = TYPE.ACK


class Den(Frame):
    def __init__(self, event=0, data=0):
        super().__init__(event=event, data=data)
        self.type = TYPE.DEN


class ControlFrame(Frame):
    event = 0
    chat_id = 0
    user_id = 0
    action = ACTION.DEFAULT
    def __init__(self, 
                 event = 0, 
                 chat_id = 0, 
                 user_id = 0, 
                 action = ACTION.DEFAULT,
                 data = 0):
        super().__init__(event=event, data=data)
        self.type = TYPE.CON
        try:
            if event or data:
                self.event   = event
                self.chat_id = int(self.mess["chat_id"])
                self.user_id = int(self.mess["user_id"])
                self.action  = self.mess["action"] 
            else:
                self.chat_id = int(chat_id)
                self.user_id = int(user_id)
                self.action  = action 
        except Exception:
            self.valid = -1

    def to_json(self):
        frame = json.dumps({
                "type"      : self.type,
                "time"      : self.time,
                "chat_id"   : self.chat_id,
                "user_id"   : self.user_id,
                "action"    : self.action
                }).encode("utf-8")
        return struct.pack("!H", len(frame))+frame


class InfoFrame(Frame):
    type = TYPE.INF
    user = None
    def __init__(self, user = None, event = 0, data = 0):
        super().__init__(event=event, data=data)
        self.user = user

        if event or data:
            self.user = User()
            self.user.from_json(self.mess["user"])

    def to_json(self):
        frame = json.dumps({
                "type": self.type,
                "time": self.time,
                "user": self.user.to_json()
                }).encode("utf-8")
        return struct.pack("!H", len(frame))+frame
    

class ChatInfoFrame(Frame):
    type = TYPE.CHI
    chat = None
    def __init__(self, chat = None, event = 0, data = 0):
        super().__init__(event=event, data=data)
        self.chat = chat

        if event or data:
            self.chat = self.mess["chat"]

    def to_json(self):
        frame = json.dumps({
                "type": self.type,
                "time": self.time,
                "chat": self.chat
                }).encode("utf-8")
        return struct.pack("!H", len(frame))+frame


class MessageFrame(Frame):
    def __init__(self, event = 0, chat_id = 0,  text = '', data = 0):
        super().__init__(event=event, data=data)
        self.type = TYPE.MES
        if event or data:
            self.chat_id = self.mess["chat_id"]
            self.text    = self.mess["text"]
        else:
            self.chat_id = chat_id
            self.text    = text

    def to_json(self):
        frame = json.dumps({
                "type":     self.type,
                "time":     self.time,
                "chat_id":  self.chat_id,
                "text":     self.text,
                }).encode("utf-8")
        return struct.pack("!H", len(frame))+frame
    

class PullFrame(Frame):
    def __init__(self, event = 0, chat_id = 0, message_id = 0, data = 0):
        super().__init__(event=event, data=data)
        self.type = TYPE.PUL
        if event or data:
            self.chat_id = self.mess["chat_id"]
            self.message_id = self.mess["message_id"]
        else:
            self.chat_id = chat_id
            self.message_id = message_id


    def to_json(self):
        frame = json.dumps({
                "type":         self.type,
                "chat_id":      self.chat_id,
                "message_id":   self.message_id,
                }).encode("utf-8")
        return struct.pack("!H", len(frame))+frame
    

class ChtFrame(Frame):
    def __init__(self, event = 0, chat_id = 0, message = 0, data = 0):
        super().__init__(event=event, data=data)
        self.type = TYPE.CHT
        if event or data:
            self.chat_id = self.mess["chat_id"]
            self.message = self.mess["message"]
        else:
            self.chat_id = chat_id
            self.message = message


    def to_json(self):
        frame = json.dumps({
                "type":         self.type,
                "chat_id":      self.chat_id,
                "message":      self.message,
                }).encode("utf-8")
        return struct.pack("!H", len(frame))+frame
    