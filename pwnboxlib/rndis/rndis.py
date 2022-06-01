import os
from pwnboxlib.proxydevice import ProxyDevice
from pwnlogger import log, log_error, log_verbose, log_warning

class RNDISProxy(ProxyDevice):
    def __init__(self, device_name: str, local_mac: str = '42:63:65:65:43:21', remote_mac: str = '42:63:65:12:34:56') -> None:
        self.local_mac = local_mac
        self.remote_mac = remote_mac
        super().__init__(device_name)


    def __load__(self):
        log_verbose(os.system(f'mkdir -p functions/{self.device_name}'))
        log_verbose(os.system(f'echo "{self.remote_mac}" > functions/{self.device_name}/host_addr'))
        log_verbose(os.system(f'echo "{self.local_mac}" > functions/{self.device_name}/dev_addr'))

        log_verbose(os.system(f'mkdir -p os_desc'))
        log_verbose(os.system(f'echo 1 > os_desc/use'))
        log_verbose(os.system(f'echo 0xbc > os_desc/b_vendor_code'))
        log_verbose(os.system(f'echo MSFT100 > os_desc/qw_sign'))

        log_verbose(os.system(f'mkdir -p functions/{self.device_name}/os_desc/interface.rndis'))
        log_verbose(os.system(f'echo RNDIS > functions/{self.device_name}/os_desc/interface.rndis/compatible_id'))
        log_verbose(os.system(f'echo 5162001 > functions/{self.device_name}/os_desc/interface.rndis/sub_compatible_id'))