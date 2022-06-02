import os
from pwnboxlib.devicefactory import DeviceFactory
from pwnlogger import log_command

class EthernetFactory(DeviceFactory):
    def __init__(self, device_name: str, local_mac: str = '42:63:65:65:43:21', remote_mac: str = '42:63:65:12:34:56') -> None:
        self.local_mac = local_mac
        self.remote_mac = remote_mac
        super().__init__(device_name)


    def __load__(self):
        log_command(f'mkdir -p functions/{self.device_name}')
        log_command(f'echo "{self.remote_mac}" > functions/{self.device_name}/host_addr')
        log_command(f'echo "{self.local_mac}" > functions/{self.device_name}/dev_addr')