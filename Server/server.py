import asyncio
import logging
import sys
import logging
import datetime
import subprocess
import struct
import json
from special_json import *


from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent, StreamDataReceived, ConnectionTerminated


try: 
    import uvloop
except ImportError:
    uvloop = None


class colors:
    RED     = '\033[91m'
    GREEN   = '\033[92m'
    YELLOW  = '\033[93m'
    BLUE    = '\033[94m'
    DEFAULT = '\033[0m'


stramid_list = []
messages = []
users = []


class SSP(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    
    def quic_send(self, stream_id, message, flag=False)->None:
        data = json.dumps(message.to_js()).encode("utf-8")
        data = struct.pack("!H", len(data))+data
        self._quic.send_stream_data(stream_id, data, end_stream=flag)
        self.transmit()


    def quic_event_received(self, event: QuicEvent):
        new_message = js_message()
        recv_mes = ''

        if isinstance(event,  StreamDataReceived):

            recv_mes = json.loads(event.data[2:].decode('utf-8'))
            if not new_message.from_js(recv_mes):
                new_message.Cond = CON.DEN

            if event.stream_id not in stramid_list:
                if new_message.Cond != CON.AUT:
                    new_message.Cond = CON.DEN
                else:
                    stramid_list.append(event.stream_id)
            

            if new_message.Cond == CON.DEN:
                new_message.Data = ''
                self.quic_send(event.stream_id, new_message, flag=True)

            elif new_message.Cond == CON.CHK:
                new_message.Data = ''
                new_message.Data = len(messages)
                new_message.Cond = CON.APP
                self.quic_send(event.stream_id, new_message)
            else:   
                new_message.Cond = CON.PLL
                messages.append(new_message.copy())

                print(colors.GREEN +\
                    f"|{datetime.datetime.now().strftime(' %H:%M:%S')}|"+\
                    f"{new_message.Cond} |"+\
                    colors.DEFAULT+f" {recv_mes}")
                
                new_message.Cond = CON.ACK
                print(messages)
                self.quic_send(event.stream_id , new_message)

                chat_dump()


def chat_dump():
    for i in messages:
        print(colors.RED,i.Name, colors.DEFAULT, end='\t')
        print(colors.BLUE, i.Time, colors.DEFAULT)
        print("-"*50)
        print(i.Data)

        
async def main(
        host:   str,
        port:   int,
        config: QuicConfiguration,
        retry:  bool,
)->None:
    logging.debug("start main")
    await serve(
        host,
        port,
        configuration   = config,
        create_protocol = SSP,
        retry           = retry,
    )
    await asyncio.Future()
    


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) != 3:
        print(f"Wrong input values: {argv}")
        exit()

    host = "127.0.0.1" if argv[1] == "d" else argv[1]
    port = 8000        if argv[2] == "d" else int(argv[2])

    config = QuicConfiguration(
        is_client=False,
        max_datagram_frame_size=65536,
    )

    config.load_cert_chain("ssl/cert.pem", 
                           "ssl/key.pem", 
                           password="kitten",
    )

    logging.debug("uvloop was assigned")
    if uvloop is not None:
        uvloop.install()
        
    logging.debug("main task was added")
    subprocess.call("clear", shell = True)

    helo = f"Server: host={host}, port={port}"
    print(colors.RED+helo+colors.DEFAULT)
    print(colors.BLUE+"~"*len(helo)+colors.DEFAULT)
    print(colors.RED+"| time    |STAT| text"+colors.DEFAULT)

    asyncio.run(
        main(
            host=host,
            port=port,
            config=config,
            retry=False,
        )
    )
