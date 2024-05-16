import sys
import time
import threading
import run

sys.path.append('.')

import _gui


if __name__ == "__main__":
    print("cpojsgohiz")
    s = ""
    with open('run.py', 'r') as f:
        for l in f.readlines():
            s += l
        s += "run()"

    _gui.startup(s)

    #_gui.call_python(a)
