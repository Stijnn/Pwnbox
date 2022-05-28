import os
import configparser
from termcolor import colored
from genericpath import exists

#
#   CONFIG PATHS
#

PWN_CONFIG_FILE_PATH = '/etc/pwnbox/pwncfg.ini'
PWN_SCRIPT_FOLDER = os.getcwd() + '/Scripts'
PWN_BOOT_SHELL_SCRIPT_FILE_PATH = PWN_SCRIPT_FOLDER + '/load_hid_kernel.sh'

RC_LOCAL_FILE_PATH = '/etc/rc.local'


def execute_os_cmd(info: str, command: str) -> int:
    exit_code = os.system(command)
    print(colored(f"[{exit_code}] Error: {info}", 'red') if exit_code != 0 else colored(f"[#] Succes: {info}", 'green'))
    return exit_code


def set_default_config():
    if exists(PWN_CONFIG_FILE_PATH):
        print(colored(f"[~] {PWN_CONFIG_FILE_PATH} already exists. Skipping creation...", "yellow"))
        return

    execute_os_cmd(
        "Setting up config directory in /etc/ for PWNBOX as /etc/pwnbox.", 
        "mkdir -p /etc/pwnbox/"
    )

    execute_os_cmd(
        "Creating default .ini file for later use. This file will hold persistent settings as to what to load on boot.", 
        f"touch {PWN_CONFIG_FILE_PATH}"
    )

    config = configparser.ConfigParser()
    config.read(PWN_CONFIG_FILE_PATH)

    config["TYPES"] = {
        "KEYBOARD": False
    }

    with open(PWN_CONFIG_FILE_PATH, 'w') as configfile:
        config.write(configfile)

    pass


def bypass_rc_local():
    with open(RC_LOCAL_FILE_PATH, 'r') as file :
        filedata = file.read()

    # Prevent duplicate writes
    if not filedata.__contains__(PWN_BOOT_SHELL_SCRIPT_FILE_PATH):
        filedata = filedata.replace('exit 0', PWN_BOOT_SHELL_SCRIPT_FILE_PATH + ' ' + os.getcwd() +" \r\nexit 0")
        with open(RC_LOCAL_FILE_PATH, 'w') as file:
            file.write(filedata)
    else:
        print(colored(f"[~] Bypass to {PWN_BOOT_SHELL_SCRIPT_FILE_PATH} already exists. Skipping creation...", "yellow"))

    pass


def main():
    set_default_config()
    bypass_rc_local()
    pass


if __name__ == "__main__":
    main()