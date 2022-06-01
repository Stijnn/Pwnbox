from pwnboxlib.proxydevice import ProxyDevice
from os import system

class StorageProxy(ProxyDevice):
    def __init__(self, device_name: str, image_location: str) -> None:
        self.image_location = image_location
        super().__init__(device_name)

    
    def __load__(self):
        system('mkdir -p ${' + self.image_location + '/img/d}')
        system('mount -o loop,ro, -t vfat ' + self.image_location + ' ${' + self.image_location + '/img/d}')
        system(f'mkdir -p functions/{self.device_name}')
        system(f'echo 1 > functions/{self.device_name}/stall')
        system(f'echo 0 > functions/{self.device_name}/lun.0/cdrom')
        system(f'echo 0 > functions/{self.device_name}/lun.0/ro')
        system(f'echo 0 > functions/{self.device_name}/lun.0/nofua')
        system(f'echo {self.image_location} > functions/{self.device_name}/lun.0/file')
        system(f'ln -s functions/{self.device_name} configs/c.1/')
