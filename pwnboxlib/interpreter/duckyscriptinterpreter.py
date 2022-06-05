from genericpath import exists
from time import sleep
from pwnboxlib.keyboard.keyboard import Keyboard
from pwnboxlib.keyboard.keytranslation import *
from pwnlogger import log_ok, log_warning


ducky_keylink_params = {
    'DELETE': KEY_DELETE, 
    'HOME': KEY_HOME, 
    'INSERT': KEY_INSERT, 
    'PAGEUP': KEY_PAGEUP, 
    'PAGEDOWN': KEY_PAGEDOWN, 
    'WINDOWS': KEY_LEFTMETA, 
    'GUI': KEY_LEFTMETA, 
    'UPARROW': KEY_UP, 
    'DOWNARROW': KEY_DOWN, 
    'LEFTARROW': KEY_LEFT, 
    'RIGHTARROW': KEY_RIGHT,
    'UP': KEY_UP, 
    'DOWN': KEY_DOWN, 
    'LEFT': KEY_LEFT, 
    'RIGHT': KEY_RIGHT, 
    'TAB': KEY_TAB,
    'BREAK': KEY_PAUSE, 
    'PAUSE': KEY_PAUSE,
    'ENTER': KEY_ENTER,
    'F1': KEY_F1,
    'F2': KEY_F2,
    'F3': KEY_F3,
    'F4': KEY_F4,
    'F5': KEY_F5,
    'F6': KEY_F6,
    'F7': KEY_F7,
    'F8': KEY_F8,
    'F9': KEY_F9,
    'F10': KEY_F10,
    'F11': KEY_F11,
    'F12': KEY_F12,
    'F13': KEY_F13,
    'F14': KEY_F14,
    'F15': KEY_F15,
    'F16': KEY_F16,
    'F17': KEY_F17,
    'F18': KEY_F18,
    'F19': KEY_F19,
    'F20': KEY_F20,
    'CAPSLOCK': KEY_CAPSLOCK,
    'END': KEY_END,
    'NUMLOCK': KEY_NUMLOCK,
    'PRINTSCREEN': KEY_SYSRQ,
    'SCROLLLOCK': KEY_SCROLLLOCK,
    'SPACE': KEY_SPACE,
    'BACKSPACE': KEY_BACKSPACE
}


ducky_mod_link = {
    'SHIFT': KEY_MOD_LSHIFT,
    'ALT': KEY_MOD_LALT,
    'CONTROL': KEY_MOD_LCTRL,
    'CTRL': KEY_MOD_LCTRL
}


def exec_ducky_function(line: str, kb: Keyboard, prev_line: str = None):
    if kb == None:
        return

    full_line_split = line.split(' ')
    function_type = full_line_split[0]

    if function_type == 'REM':
        return

    elif function_type == '':
        return

    elif function_type == 'STRING':
        kb.write(" ".join(list(full_line_split[1:])))

    # elif function_type == 'DEFAULT_DELAY' or function_type == 'DEFAULTDELAY':
    #     sleep(float(full_line_split[1]) / 100)

    elif function_type == 'DELAY':
        sleep(float(full_line_split[1]) / 1000)

    elif function_type == 'GUI' or function_type == 'WINDOWS':
        key_data = USB_CHARACTER_TRANSLATION_KEYCODES.get(full_line_split[1])
        if key_data:
            kb.press_key(chr(key_data[1]), [KEY_MOD_LMETA])

    elif function_type == 'MENU' or function_type == 'APP':
        kb.press_key(KEY_F10, [KEY_MOD_LSHIFT])

    elif function_type == 'SHIFT' or function_type == 'ALT' or function_type == 'CONTROL' or function_type == 'CTRL':
        if len(full_line_split) > 1:
            if full_line_split[1] in ducky_keylink_params:
                kb.press_key(ducky_keylink_params.get(full_line_split[1]), [ducky_mod_link.get(function_type)])
            elif full_line_split[1] in USB_CHARACTER_TRANSLATION_KEYCODES:
                kb.press_key(chr(USB_CHARACTER_TRANSLATION_KEYCODES[full_line_split[1]][1]), [ducky_mod_link.get(function_type)])
            else:
                kb.press_key(full_line_split[1], [ducky_mod_link.get(function_type)])
        else:
            kb.press_key(KEY_NONE, [ducky_mod_link.get(function_type)])

    elif function_type in ducky_mod_link:
        if len(full_line_split) == 1:
            kb.press_key(KEY_NONE, [ducky_mod_link[function_type]])
        elif len(full_line_split) > 1:
            if full_line_split[1] in ducky_keylink_params:
                kb.press_key(ducky_keylink_params[full_line_split[1]], [ducky_mod_link[function_type]])
            elif full_line_split[1] in USB_CHARACTER_TRANSLATION_KEYCODES:
                kb.press_key(chr(USB_CHARACTER_TRANSLATION_KEYCODES[full_line_split[1]][1]), [ducky_mod_link[function_type]])
            else:
                kb.press_key(KEY_NONE, [ducky_mod_link[function_type]])

    elif function_type in ducky_keylink_params:
        kb.press_key(ducky_keylink_params[function_type], [])

    elif function_type == 'REPEAT':
        if prev_line != None:
            for r in range(int(full_line_split[1])):
                exec_ducky_function(line, kb)

    else:
        log_warning(f'Unknown case command: {function_type} and {full_line_split[1:]}')


class DuckyScriptInterpeter:
    @staticmethod
    def exec_script(script_file_path: str) -> bool:
        log_ok(f'Running: {script_file_path}')

        if not exists(script_file_path):
            return False

        keyboard_device = Keyboard.get()
        if keyboard_device == None:
            return False

        script_lines = []

        file_handle = open(script_file_path, 'r')
        lines = file_handle.readlines()
        for l in lines:
            script_lines.append(l.strip())
        file_handle.close()

        delay_per_func = 0.0

        for l in script_lines:
            if l.split(' ')[0] == 'DEFAULT_DELAY' or l.split(' ')[0] == 'DEFAULTDELAY':
                delay_per_func = float(l.split[1]) / 100

        for l in script_lines:
            exec_ducky_function(l, keyboard_device)
            sleep(delay_per_func)

        return True