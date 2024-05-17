import asyncio
import logging
import ssl
import sys
from typing import cast

from aioquic.asyncio.client import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent, StreamDataReceived

from src.myjson import *
from src.chatlist import *
from random import randint

class User(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stream_id = self._quic.get_next_available_stream_id()
        self.message_buffer = []

    async def send(self, frame: bytes) -> None:
        self._quic.send_stream_data(self.stream_id, frame, end_stream=False)
        self.transmit()

    def quic_event_received(self, event: QuicEvent):
        if isinstance(event, StreamDataReceived):
            print(event.data.decode())
            

async def user_input(client: User):
    while True:
        frame = input().encode()
        await client.send(frame)
        await asyncio.sleep(0.1)

async def main(
        config: QuicConfiguration,
        host: str,
        port: int,
        local_port: int,
) -> None:
    async with connect(
        host,
        port,
        configuration=config,
        local_port=local_port,
        wait_connected=True,
        create_protocol=User
    ) as client:
        client = cast(User, client)
        input_task = asyncio.create_task(user_input(client))
        await input_task

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) != 4:
        print(f"Wrong input values: {argv}")
        exit()

    host = "127.0.0.1" if argv[1] == "d" else argv[1]
    port = 8000 if argv[2] == "d" else int(argv[2])
    uport = randint(1000, 65000)

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
