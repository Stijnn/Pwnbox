from os.path import exists
from time import sleep
from typing import List

from pwncore.pwncore import USBDevice
from keyboard.key_translation import USB_CHARACTER_TRANSLATION_KEYCODES, KeyboardModifiers, KeyboardKeys


class Keyboard(USBDevice):
    def __init__(self, gadget_path) -> None:
        if exists(gadget_path):
            super().__init__({
                "gadget_path": gadget_path
            })
        else:
            super().__init__({
                "gadget_path": None
            })
        pass


    def __open_device__(self):
        if self.gadget == None:
            self.gadget = open(self.__device_info__['gadget_path'], 'wb') 
        return self.gadget


    def __close_device__(self):
        if self.gadget:
            self.gadget.close()
            self.gadget = None
        pass


    def __write__(self, data):
        d = self.__open_device__()
        d.write(data)
        self.__close_device__()
        pass


    def __write_char__(self, character: str):
        key_meta_data = USB_CHARACTER_TRANSLATION_KEYCODES.get(character)
        if key_meta_data == None:
            return

        key_buffer = bytes(8)

        if key_meta_data[0]:
            key_buffer[0] |= KeyboardModifiers.KEY_MOD_LSHIFT
        
        key_buffer[2] = bytes([key_meta_data[1]])

        self.__write__(key_buffer[0:8])
        sleep(0.0001)
        self.release_keys()
        pass


    def send_text(self, text: str):
        for c in text:
            self.__send_char__(c)
        pass


    def release_keys(self):
        d = self.__open_device__()
        d.write(bytes(8))
        self.__close_device__()
        pass


    def press_key(self, key: KeyboardKeys, modifiers: List[KeyboardModifiers], release=True):
        b = bytes(8)
        for mod in modifiers:
            b[0] |= mod
        b[2] = key
        self.__write__(b)
        if release:
            sleep(0.0001)
            self.release_keys()
        pass
