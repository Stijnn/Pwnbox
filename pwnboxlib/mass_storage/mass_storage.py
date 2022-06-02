from pwnboxlib.devicefactory import DeviceFactory
from pwnlogger import log_command

class StorageFactory(DeviceFactory):
    def __init__(self, device_name: str, image_location: str) -> None:
        self.image_location = image_location
        super().__init__(device_name)

    
    def __load__(self):
        log_command(f'mkdir -p functions/{self.device_name}')
        log_command(f'echo 1 > functions/{self.device_name}/stall')
        log_command(f'echo 0 > functions/{self.device_name}/lun.0/cdrom')
        log_command(f'echo 0 > functions/{self.device_name}/lun.0/ro')
        log_command(f'echo 0 > functions/{self.device_name}/lun.0/nofua')
        log_command(f'echo {self.image_location} > functions/{self.device_name}/lun.0/file')
