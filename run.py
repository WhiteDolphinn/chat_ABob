import asyncio
#import logging
import sys
import logging

#import datetime
#import json

#import random

from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent, StreamDataReceived, ConnectionTerminated

#import server.src.dump
#import server.src.userlist
#import server.src.chatlist
#import server.src.user
#from   server.src.myjson import *


try: import uvloop
except ImportError: uvloop = None

import user


def run():
    host = "185.198.152.16"

    if len(sys.argv) > 1:
        if sys.argv[1] == "-l":
            host = "127.0.0.1"

    port = 8000

    config = QuicConfiguration(
        is_client=True,
        max_datagram_frame_size=65536,)

    config.load_cert_chain("ssl/cert.pem", 
                        "ssl/key.pem", 
                        password="kitten",)

    if uvloop is not None:
        uvloop.install()

    asyncio.run(
        user.main(host=host,
            port=port,
            config=config,
            retry=False,
        )
    )
    return
    print("print")
    print("print2")
    print(_gui.get_username(), "zhopa1")
    _gui.push_chat("pupa")
    #_gui.push_chat("puupa0")
    _gui.push_chat("puupa1")
    _gui.push_chat("puupa2")
    _gui.push_message("pupa", "lupa1")
    #time.sleep(3)
    _gui.push_message("puupa1", "luupa1")
    #time.sleep(10)
    _gui.push_message("puupa1", "lupa2")
    #time.sleep(10)
    _gui.push_message("puupa1", "luupa2")
    return
