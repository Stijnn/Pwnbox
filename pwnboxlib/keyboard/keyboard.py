import os
from os.path import exists
from time import sleep
from typing import List

from pwnboxlib.keyboard.keytranslation import *
from pwnboxlib.devicefactory import DeviceFactory
from pwnlogger import log_command


class KeyboardFactory(DeviceFactory):
    def __init__(self, device_name: str) -> None:
        super().__init__(device_name)

    
    def __load__(self):
        log_command(f'echo 1 > functions/{self.device_name}/protocol')
        log_command(f'echo 1 > functions/{self.device_name}/subclass')
        log_command(f'echo 8 > functions/{self.device_name}/report_length')
        log_command(f'echo -ne \\x05\\x01\\x09\\x06\\xa1\\x01\\x05\\x07\\x19\\xe0\\x29\\xe7\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x08\\x81\\x02\\x95\\x01\\x75\\x08\\x81\\x03\\x95\\x05\\x75\\x01\\x05\\x08\\x19\\x01\\x29\\x05\\x91\\x02\\x95\\x01\\x75\\x03\\x91\\x03\\x95\\x06\\x75\\x08\\x15\\x00\\x25\\x65\\x05\\x07\\x19\\x00\\x29\\x65\\x81\\x00\\xc0 > functions/{self.device_name}/report_desc')


class Keyboard:
    def __init__(self, gadget_path) -> None:
        self.__device_info__ = {
            "gadget_path": gadget_path
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
            if meta == None:
                continue

            if meta[0]:
                b[0] = chr(ord(b[0]) + ord(KEY_MOD_LSHIFT))
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