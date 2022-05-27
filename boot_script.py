import configparser
import os

CONFIG_PATH = '/etc/pwnbox/pwncfg.ini'

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

boot_config = {
    {
        "id": "HID_KEYBOARD",
        "should_load": config.getboolean('TYPES', 'KEYBOARD'),
        "load_file": "./load_keyboard_kernel.sh"
    }
}

def main():

    for boot_object in boot_config:
        try:
            if boot_object.should_load:
                os.system(boot_object.load_file)
        except:
            print(f"Failed loading: {boot_object.id}")

    pass


if __name__ == "__main__":
    main()