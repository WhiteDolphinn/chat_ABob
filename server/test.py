import asyncio
import logging
import ssl
import sys
from random import randint
from typing import cast

from aioquic.asyncio.client import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent, StreamDataReceived

from src.myjson import *

class User(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stream_id = None
        self.uesrname = None
        self.message_buffer = []

    
    async def sync(self, argv):
        self.stream_id = self._quic.get_next_available_stream_id()
        frame = Sig(name=argv[2], password=argv[3])
        for i in range(100):
            await self.send(frame)
            await asyncio.sleep(3)


    async def send(self, frame)->None:
        print(frame)
        self._quic.send_stream_data(self.stream_id, frame.to_json(), end_stream=False)
        self.transmit()

    def quic_event_received(self, event: QuicEvent):
        if isinstance(event, StreamDataReceived):
            frame = Frame(event).from_json()
            print(frame) 


async def main(
        config: QuicConfiguration,
        host: str,
        port: int,
        argv: list,
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
        await client.sync(argv)
        await asyncio.sleep(10)
    

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) < 2:
        print(f"Wrong input values: {argv}")
        exit()

    host = "127.0.0.1" if argv[1] == "-l" else "185.198.152.16"
    port = 8000     
    uport= randint(2000, 6553)        
    message = argv[2]

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
            argv=argv,
            local_port=uport,
        )
    )