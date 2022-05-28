import configparser
import os
import logging
import sys

from datetime import datetime

SCRIPT_DIR = os.getcwd() + "/Scripts"
SCRIPT_KEYBOARD = SCRIPT_DIR + "/load_keyboard_kernel.sh"

LOGGING_DIR = os.getcwd() + "/Logs"
os.mkdir(LOGGING_DIR)
logging.basicConfig(filename=f'{LOGGING_DIR}/{datetime.now()}_boot.log', encoding='utf-8', level=logging.DEBUG)

CONFIG_PATH = '/etc/pwnbox/pwncfg.ini'

# Retrieve GADGET_PATH from CLI
if len(sys.argv) > 1:
    GADGET_PATH = sys.argv[1]

config = configparser.ConfigParser()
config.read(CONFIG_PATH)
logging.info(f"Read {CONFIG_PATH} as CONFIG_PATH for {config}")

boot_config = [
    {
        "id": "HID_KEYBOARD",
        "should_load": config.getboolean('TYPES', 'KEYBOARD'),
        "load_file": SCRIPT_KEYBOARD
    }
]
logging.info(f"Setup bootconfig based on {config} result\n{boot_config}")


def main():

    for boot_object in boot_config:
        try:
            if boot_object['should_load']:
                os.system(boot_object["load_file"])
        except:
            logging.error(f"Failed loading: { boot_object['id'] }")

    pass


if __name__ == "__main__":
    main()