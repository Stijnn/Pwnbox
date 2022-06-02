import os


class DeviceFactory:
    def __init__(self, device_name: str) -> None:
        self.device_name = device_name
        pass


    def __create_dir__(self):
        return os.system(f'mkdir -p functions/{self.device_name}')


    def __load__(self):
        pass


    def __link__(self):
        return os.system(f'ln -s functions/{self.device_name} configs/c.1/')


    def build(self):
        self.__create_dir__()
        self.__load__()
        self.__link__()
        pass