import asyncio
import logging
import sys
import logging


from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent, StreamDataReceived, ConnectionTerminated

import src.dump
import src.userlist
import src.chatlist
import src.user
from   src.myjson import *


try: import uvloop
except ImportError: uvloop = None


class SSP(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users_db = src.userlist.UsersList()
        self.chats_db = src.chatlist.ChatList()
        self.user     = None


    def quic_send(self, stream_id, frame, flag=False)->None:
        self._quic.send_stream_data(stream_id, frame.to_json(), end_stream=flag)
        self.transmit()


    def quic_event_received(self, event: QuicEvent):
        if isinstance(event,  StreamDataReceived):
            src.dump.event(event_=event)
            frame = Frame(event).from_json()
            src.dump.frame_dump(frame)

            if frame.type == TYPE.SIG:
                self.sing_up(frame=frame, event=event)
            elif self.user == None:
                self.quic_send(event.stream_id, Den())
            elif frame.type == TYPE.CON:
                self.chat_control(frame=frame, event=event)


    def sing_up(self, frame: Sig, event: StreamDataReceived):
        if self.user != None:
            answer = InfoFrame(self.user)
        else:
            result = self.users_db.add(frame=frame)
            if result == TYPE.DEN:
                answer = Den()
            else:
                self.user = result
                answer = InfoFrame(self.user)
        self.quic_send(event.stream_id, answer)


    def chat_control(self, frame: ControlFrame, event: StreamDataReceived):
        if frame.action == ACTION.CREAT:
            chat_id = self.chats_db.add(self.user)
            self.users_db.update_user(self.user)

            answer = Ack()
            self.quic_send(event.stream_id, answer)
        else:
            chat = src.chatlist.Chat()
            chat.from_json(self.chats_db.find(frame.chat_id)[0][2])

            if frame.action == ACTION.ADD:
                user = src.user.User()
                user.from_json(self.users_db.find(id=frame.user_id)[3])
                answer = chat.add_user(self.user, user)
                if isinstance(answer, Ack):
                    if frame.chat_id not in user.chats:
                        user.chats.append(int(frame.chat_id))
                        self.users_db.update_user(user)
                    self.chats_db.update_chat(chat)
                self.quic_send(event.stream_id, answer)

            if frame.action == ACTION.BUN:
                user = src.user.User()
                user.from_json(self.users_db.find(id=frame.user_id)[3])
                answer = chat.del_user(self.user, user)
                if isinstance(answer, Ack):
                    if frame.chat_id in user.chats:
                        user.chats.remove(frame.chat_id)
                        self.users_db.update_user(user)
                    self.chats_db.update_chat(chat)
                self.quic_send(event.stream_id, answer)

            if frame.action == ACTION.EXIT:
                if chat.admin_id == self.user.id:
                    answer = Den()
                else:
                    print("eee")
                    user = self.user
                    answer = chat.ext_user(user)
                    if isinstance(answer, Ack):
                        if frame.chat_id in user.chats:
                            user.chats.remove(frame.chat_id)
                            self.users_db.update_user(user)
                        self.chats_db.update_chat(chat)
                self.quic_send(event.stream_id, answer)

            if frame.action == ACTION.DEL:
                if chat.admin_id != self.user.id:
                    answer = Den()
                else:
                    for i in chat.userlist:
                        user = src.user.User()
                        user.from_json(self.users_db.find(id=i)[3])
                        if frame.chat_id in user.chats:
                            user.chats.remove(frame.chat_id)
                            self.users_db.update_user(user)
                    self.chats_db.delite_chat(chat)
                self.quic_send(event.stream_id, Ack())

            if frame.action == ACTION.INFO:
                self.quic_send(event.stream_id, ChatInfoFrame(chat=chat.to_json()))


            


async def main(
        host:   str,
        port:   int,
        config: QuicConfiguration,
        retry:  bool,
)->None:
    
    await serve(
        host,
        port,
        configuration   = config,
        create_protocol = SSP,
        retry           = retry,
    )
    await asyncio.Future()
    src.dump.final()


if __name__ != "__main__":
    exit(0)

host = "185.198.152.16"

if len(sys.argv) > 1:
    if sys.argv[1] == "-l":
        host = "127.0.0.1"

port = 8000

config = QuicConfiguration(
    is_client=False,
    max_datagram_frame_size=65536,)

config.load_cert_chain("ssl/cert.pem", 
                       "ssl/key.pem", 
                       password="kitten",)

if uvloop is not None:
    uvloop.install()

src.dump.hello(host, port)

asyncio.run(
    main(host=host,
         port=port,
         config=config,
         retry=False,
    )
)