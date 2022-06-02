import os
from pwnboxlib.devicefactory import DeviceFactory
from pwnlogger import log_command

class RNDISFactory(DeviceFactory):
    def __init__(self, device_name: str, local_mac: str = '42:63:65:65:43:21', remote_mac: str = '42:63:65:12:34:56') -> None:
        self.local_mac = local_mac
        self.remote_mac = remote_mac
        super().__init__(device_name)


    def __load__(self):
        log_command(f'mkdir -p functions/{self.device_name}')
        log_command(f'echo "{self.remote_mac}" > functions/{self.device_name}/host_addr')
        log_command(f'echo "{self.local_mac}" > functions/{self.device_name}/dev_addr')

        log_command(f'mkdir -p os_desc')
        log_command(f'echo 1 > os_desc/use')
        log_command(f'echo 0xbc > os_desc/b_vendor_code')
        log_command(f'echo MSFT100 > os_desc/qw_sign')

        log_command(f'mkdir -p functions/{self.device_name}/os_desc/interface.rndis')
        log_command(f'echo RNDIS > functions/{self.device_name}/os_desc/interface.rndis/compatible_id')
        log_command(f'echo 5162001 > functions/{self.device_name}/os_desc/interface.rndis/sub_compatible_id')