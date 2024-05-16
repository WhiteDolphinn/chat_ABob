import sys
import time
import threading

sys.path.append('.')

import _gui

a = """
def run():
    print("print")
    time.sleep(4)
    print("print2")
    return
    print(_gui.get_username(), "zhopa1")
    _gui.push_chat("pupa")
    _gui.push_chat("puupa")
    _gui.push_chat("ppupa")
    _gui.push_message("pupa", "lupa1")
    _gui.push_message("puupa", "luupa1")
    _gui.push_message("pupa", "lupa2")
    _gui.push_message("puupa", "luupa2")
run()
"""

#thread = threading.Thread(target=run)
#thread.start()

print("cpojsgohiz")
_gui.call_python(a)
#_gui.mainloop()

# a = _c_python.c_python(12, 3.14, 0x30)
# a.print(a)
# a.print(a)
# _c_python.func_print(2, 3.0, 0x36)
# print(a.val1)
# # a.func_print()
# # _c_python.c_python.func_print()
# class Gui:
#     def __init__(self):
#         self.a = 5
#         self.b = "zhopa"

#     def print(self):
#         print(self.a)
#         print(self.b)
