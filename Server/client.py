import asyncio
import logging
import ssl
import struct
import sys
from typing import cast
import json
from special_json import *

from aioquic.asyncio.client import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent, StreamDataReceived

# logging.basicConfig(level=logging.DEBUG)


class User(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stream_id = None
        self.uesrname = None
        self.message_buffer = []

    
    async def sync(self, name):
        self.stream_id = self._quic.get_next_available_stream_id()
        data = js_message(CON.AUT, name, data=input("Mes:"))
        await self.send(json.dumps(data.to_js()))


    async def send(self, message)->None:
        data = message.encode("utf-8")
        data = struct.pack("!H", len(data))+data
        self._quic.send_stream_data(self.stream_id, data, end_stream=False)

        self.transmit()

    def quic_event_received(self, event: QuicEvent):
        if isinstance(event, StreamDataReceived):
            recv_mes = event.data[2:].decode('utf-8')
            print(recv_mes) 



async def main(
        config: QuicConfiguration,
        host: str,
        port: int,
        message: str,
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
        await client.sync(message)
        await asyncio.sleep(0.1)
    

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) != 5:
        print(f"Wrong input values: {argv}")
        exit()

    host = "127.0.0.1" if argv[1] == "d" else argv[1]
    port = 8000        if argv[2] == "d" else int(argv[2])
    uport= 2000        if argv[3] == "d" else int(argv[3])
    message = argv[4]

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
            message=message,
            local_port=uport,
        )
    )