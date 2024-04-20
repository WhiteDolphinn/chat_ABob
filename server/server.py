import asyncio
import logging
import sys
import logging


from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent, StreamDataReceived, ConnectionTerminated

import src.dump
import src.mysql
import src.user
from   src.myjson import *


try: import uvloop
except ImportError: uvloop = None


class SSP(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users_db = src.mysql.UsersList()
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
                self.quic_send(event.stream_id, Den(), True)
            elif frame.type == TYPE.CON:
                self.chat_control(frame=frame, event=event)


    def sing_up(self, frame: Sig, event: StreamDataReceived):
        if self.user != None:
            answer = Ack()
        else:
            result = self.users_db.add(frame=frame)
            if result == TYPE.DEN:
                answer = Den()
            else:
                answer = Ack()
                self.user = result
        self.quic_send(event.stream_id, answer)


    def chat_control(self, frame: ControlFrame, event: StreamDataReceived):
        pass


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