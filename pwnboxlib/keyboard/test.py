from time import sleep
from keyboard.keyboard import Keyboard
from keyboard.keytranslation import *

kb = Keyboard('/dev/hidg0')
kb.press_key(KEY_NONE, [KEY_LEFTMETA])
sleep(0.1)
kb.write('cmd')
sleep(0.1)
kb.write_line('ping 192.168.1.9')