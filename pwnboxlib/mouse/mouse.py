from genericpath import exists
import math
import os
from pwnboxlib.devicefactory import DeviceFactory
from pwnlogger import log_command

class MouseFactory(DeviceFactory):
    def __init__(self, device_name: str) -> None:
        super().__init__(device_name)

    
    def __load__(self):
        log_command(f'echo 2 > functions/{self.device_name}/protocol')
        log_command(f'echo 1 > functions/{self.device_name}/subclass')
        log_command(f'echo 6 > functions/{self.device_name}/report_length')
        with open(f'functions/{self.device_name}/report_desc', 'wb') as report_desc:
            report_desc.write(b'\x05\x01\x09\x02\xa1\x01\x09\x01\xa1\x00\x05\x09\x19\x01\x29\x03\x15\x00\x25\x01\x95\x03\x75\x01\x81\x02\x95\x01\x75\x05\x81\x01\x05\x01\x09\x30\x09\x31\x09\x38\x15\x81\x25\x7f\x75\x08\x95\x03\x81\x06\xc0\xc0')


class Mouse():
    @staticmethod
    def get():
        if exists('/tmp/pwnbox/mouse'):
            with open('/tmp/pwnbox/mouse', 'r') as tmpfile:
                device_name = tmpfile.readline().strip()
                return Mouse(device_name) 
        else:
            return None


    def __init__(self, gadget_path) -> None:
        self.__device_info__ = {
            "gadget_path": gadget_path
        }
        self.gadget = None
        pass


    def __create_report__(self):
        return chr(0)*3


    def __write__(self, report: str):
        with open(self.__device_info__['gadget_path'], 'wb+') as file:
            file.write(report.encode())
        pass


    def __write_zero_report__(self):
        self.__write__(self.__create_report__())
        pass


    def move_mouse(self, x: int = 0, y: int = 0):
        rem_x = x, rem_y = y
        for idx in range(math.ceil(x / 0xFF) if x > y else math.ceil(y / 0xFF)):
            report      = list(self.__create_report__())
            report[1]   = chr(0xFF if rem_x > 0xFF else rem_x)
            report[2]   = chr(0xFF if rem_y > 0xFF else rem_y)
            self.__write__("".join(report))
            rem_x -= 0xFF if rem_x > 0xFF else rem_x
            rem_y -= 0xFF if rem_y > 0xFF else rem_y