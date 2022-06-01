import math
import os
from pwnboxlib.proxydevice import ProxyDevice
from pwnlogger import log, log_error, log_verbose, log_warning

class MouseProxy(ProxyDevice):
    def __init__(self, device_name: str) -> None:
        super().__init__(device_name)

    
    def __load__(self):
        log_verbose(os.system(f'echo 2 > functions/{self.device_name}/protocol'))
        log_verbose(os.system(f'echo 1 > functions/{self.device_name}/subclass'))
        log_verbose(os.system(f'echo 6 > functions/{self.device_name}/report_length'))
        log_verbose(os.system(f'echo -ne \\x05\\x01\\x09\\x02\\xa1\\x01\\x09\\x01\\xa1\\x00\\x05\\x09\\x19\\x01\\x29\\x03\\x15\\x00\\x25\\x01\\x95\\x03\\x75\\x01\\x81\\x02\\x95\\x01\\x75\\x05\\x81\\x01\\x05\\x01\\x09\\x30\\x09\\x31\\x09\\x38\\x15\\x81\\x25\\x7f\\x75\\x08\\x95\\x03\\x81\\x06\\xc0\\xc0 > functions/{self.device_name}/report_desc'))


class Mouse():
    def __init__(self, gadget_path) -> None:
        self.__device_info__ = {
            "gadget_path": gadget_path
        }
        self.gadget = None
        pass


    def __create_report__(self):
        return chr(0)*3


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


    def move_mouse(self, x: int = 0, y: int = 0):
        rem_x = x, rem_y = y
        for idx in range(math.ceil(x / 0xFF) if x > y else math.ceil(y / 0xFF)):
            report      = list(self.__create_report__())
            report[1]   = chr(0xFF if rem_x > 0xFF else rem_x)
            report[2]   = chr(0xFF if rem_y > 0xFF else rem_y)
            self.__write__("".join(report))
            rem_x -= 0xFF if rem_x > 0xFF else rem_x
            rem_y -= 0xFF if rem_y > 0xFF else rem_y