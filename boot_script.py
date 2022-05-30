import configparser
from genericpath import exists
import os
import logging
import sys

from datetime import datetime
from time import sleep

SCRIPT_DIR = os.getcwd() + "/Scripts"
SCRIPT_KEYBOARD = SCRIPT_DIR + "/load_keyboard_kernel.sh"

LOGGING_DIR = os.getcwd() + "/Logs"

if not exists(LOGGING_DIR):
    os.mkdir(LOGGING_DIR)

logging.basicConfig(filename=f'{LOGGING_DIR}/{datetime.now()}_boot.log', encoding='utf-8', level=logging.DEBUG)

CONFIG_PATH = '/etc/pwnbox/pwncfg.ini'
ROOT_PATH = os.getcwd()

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

    idx = 0
    for boot_object in boot_config:
        try:
            if boot_object['should_load']:
                os.chdir(GADGET_PATH)
                exit_code = os.system(boot_object["load_file"] + f' {idx}')
                os.chdir(ROOT_PATH)
                if exit_code == 0:
                    logging.info(f"Loaded the following USB Gadget: {boot_object}")
                    idx += 1
        except:
            logging.error(f"Failed loading: { boot_object['id'] }")

    sleep(10)
    os.system(f'{ROOT_PATH}/Scripts/post_boot_script.sh {ROOT_PATH}')

    pass


if __name__ == "__main__":
    main()