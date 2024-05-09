import asyncio
import logging
import ssl
import sys
import os
from typing import cast

from aioquic.asyncio.client import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent, StreamDataReceived

from src.myjson import *
from src.chatlist import *

class User(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stream_id = None
        self.uesrname = None
        self.message_buffer = []
        self.user = None
        self.chat = None

    async def loop(self):
        action = input("Get action:")
        if action == "sync":
            await self.sync()
        elif action == "create":
            await self.create_chat()
        elif action == "add":
            await self.add_user_to_chat()
        elif action == "bun":
            await self.bun_user_to_chat()
        elif action == "exit":
            await self.exit_from_chat()
        elif action == "del":
            await self.del_chat()
        elif action == "chat":
            await self.get_info_chat()
        else: 
            self.loop()
        


    async def sync(self):
        name        = input("Print name    :")
        password    = input("Print password:")
        self.stream_id = self._quic.get_next_available_stream_id()
        frame = Sig(name=name, password=password)
        await self.send(frame)

    async def create_chat(self):
        frame = ControlFrame(action=ACTION.CREAT)
        await self.send(frame)

    async def add_user_to_chat(self):
        chat_id = input("chat id:")
        user_id = input("user id:")
        frame = ControlFrame(action=ACTION.ADD, user_id=user_id, chat_id=chat_id)
        await self.send(frame)

    async def bun_user_to_chat(self):
        chat_id = input("chat id:")
        user_id = input("user id:")
        frame = ControlFrame(action=ACTION.BUN, user_id=user_id, chat_id=chat_id)
        await self.send(frame)

    async def exit_from_chat(self):
        chat_id = input("chat id:")
        frame = ControlFrame(action=ACTION.EXIT, chat_id=chat_id)
        await self.send(frame)

    async def del_chat(self):
        chat_id = input("chat id:")
        frame = ControlFrame(action=ACTION.DEL, chat_id=chat_id)
        await self.send(frame)

    async def get_info_chat(self):
        chat_id = input("chat id:")
        frame = ControlFrame(action=ACTION.INFO, chat_id=chat_id)
        await self.send(frame)


    async def send(self, frame)->None:
        self._quic.send_stream_data(self.stream_id, frame.to_json(), end_stream=False)
        self.transmit()
        await asyncio.sleep(0.1)
        await self.loop()

    def quic_event_received(self, event: QuicEvent):
        if isinstance(event, StreamDataReceived):
            print(event.data[2:].decode('utf-8'))
            frame = Frame(event).from_json()
            print(type(frame))
            if isinstance(frame, InfoFrame):
                self.user = frame.user
            if isinstance(frame, ChatInfoFrame):
                self.chat = Chat()
                self.chat.from_json(frame.mess["chat"])
                print(self.chat.userlist)

            



async def main(
        config: QuicConfiguration,
        host: str,
        port: int,
        local_port: int,
)->None:
    async with connect(
        host,
        port,
        configuration=config,
        local_port=local_port,
        wait_connected= True,
        create_protocol=User
    ) as client:
        client = cast(User, client)
        await client.loop()
        await asyncio.sleep(0.1)


if __name__ == "__main__":
    os.system("clear")
    argv = sys.argv
    if len(argv) != 4:
        print(f"Wrong input values: {argv}")
        exit()

    host = "127.0.0.1" if argv[1] == "d" else argv[1]
    port = 8000        if argv[2] == "d" else int(argv[2])
    uport= 2000        if argv[3] == "d" else int(argv[3])

    config = QuicConfiguration(
        is_client=True,
        max_datagram_frame_size=65536,
    )
    config.verify_mode = ssl.CERT_NONE

    logging.debug("main task was added")
    asyncio.run(
        main(
            host=host,
            port=port,
            config=config,
            local_port=uport,
        )
    )