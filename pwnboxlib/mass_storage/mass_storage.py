from pwnboxlib.proxydevice import ProxyDevice
from pwnlogger import log, log_error, log_verbose, log_warning
from os import system

class StorageProxy(ProxyDevice):
    def __init__(self, device_name: str, image_location: str) -> None:
        self.image_location = image_location
        super().__init__(device_name)

    
    def __load__(self):
        log(system('mkdir -p ${' + self.image_location + '/img/d}'))
        log(system('mount -o loop,ro, -t vfat ' + self.image_location + ' ${' + self.image_location + '/img/d}'))
        log(system(f'mkdir -p functions/{self.device_name}'))
        log(system(f'echo 1 > functions/{self.device_name}/stall'))
        log(system(f'echo 0 > functions/{self.device_name}/lun.0/cdrom'))
        log(system(f'echo 0 > functions/{self.device_name}/lun.0/ro'))
        log(system(f'echo 0 > functions/{self.device_name}/lun.0/nofua'))
        log(system(f'echo {self.image_location} > functions/{self.device_name}/lun.0/file'))
        log(system(f'ln -s functions/{self.device_name} configs/c.1/'))
