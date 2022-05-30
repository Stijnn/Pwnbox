from os.path import exists
from time import sleep
from typing import List

from keytranslation import *

class Keyboard():
    def __init__(self, gadget_path) -> None:
        if exists(gadget_path):
            self.__device_info__ = {
                "gadget_path": gadget_path
            }
        else:
            self.__device_info__ = {
                "gadget_path": None
            }
        self.gadget = None
        pass


    def __create_report__(self):
        return KEY_NONE*8


    def __open_device__(self):
        if self.gadget == None:
            self.gadget = open(self.__device_info__['gadget_path'], 'wb+') 
        return self.gadget


    def __close_device__(self):
        if self.gadget:
            self.gadget.close()
            self.gadget = None
        pass


    def __write__(self, report: str):
        d = self.__open_device__()
        d.write(report.encode())
        self.__close_device__()
        pass


    def __write_zero_report__(self):
        self.__write__(self.__create_report__())
        pass


    def __write_text__(self, text: str):
        for c in text:
            b = list(self.__create_report__())
            meta = USB_CHARACTER_TRANSLATION_KEYCODES.get(c)
            if meta[0]:
                b[0] = chr(ord(b[0]) + KEY_MOD_LSHIFT)
            b[2] = chr(meta[1])
            self.__write__("".join(b))
            sleep(0.001)
            self.__write_zero_report__()
        pass


    def write(self, text: str):
        self.__write_text__(text)
        pass


    def write_line(self, text: str):
        self.__write_text__(text)
        sleep(0.001)
        self.__write_zero_report__()
        sleep(0.001)
        enter_report    = list(self.__create_report__())
        enter_report[2] = KEY_ENTER
        self.__write__("".join(enter_report))

    
    def press_key(self, key: str, modifiers: List[str] = [KEY_NONE], release=True):
        report = list(self.__create_report__())
        
        for mod in modifiers:
            if len(mod) == 1:
                report[0] = chr(ord(report[0]) + ord(mod))
        
        report[2] = key
        self.__write__("".join(report))
        if release:
            sleep(0.001)
            self.__write_zero_report__()

        pass