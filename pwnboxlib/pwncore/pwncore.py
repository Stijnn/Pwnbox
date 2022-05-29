class USBDeviceFunction:
    def __init__(self) -> None:
        pass


class USBDevice:
    def __init__(self, device_info: dict) -> None:
        self.__device_info__ = device_info
        pass


    def get_functions(self):
        return []