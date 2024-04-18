import datetime
import subprocess
import os
from aioquic.quic.events import QuicEvent, StreamDataReceived, ConnectionTerminated


class colors:
    RED     = '\033[91m'
    GREEN   = '\033[92m'
    YELLOW  = '\033[93m'
    BLUE    = '\033[94m'
    DEFAULT = '\033[0m'


def hello(host, port):
    subprocess.call("clear")
    print(colors.RED+
          f"host:{host}",
          f"\tport: {port}",
          f"\ntime:{datetime.datetime.now().strftime(' %H:%M:%S')}",
          f"\t\tmes:",
          "server turning on",
          colors.DEFAULT)
    print('-'*os.get_terminal_size().columns)


def event(event_):
    print(f"time:{datetime.datetime.now().strftime(' %H:%M:%S')}",
          colors.GREEN+
          f"\t\tmes:",
          f"user {event_.stream_id} is writing",
          colors.DEFAULT)


def users():
    pass


def chats():
    pass


def final():
    print(colors.RED+
          f"\ntime:{datetime.datetime.now().strftime(' %H:%M:%S')}",
          f"\t\tmes:",
          "server shutdown",
          colors.DEFAULT)