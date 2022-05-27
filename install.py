import os
import configparser
import json
from termcolor import colored

def execute_os_cmd(info: str, command: str):
    r = os.system(command)
    print(colored(f"[!] Error: {info} failed with EXIT_CODE: {r}", 'red') if r != 0 else colored(f"[#] Succes: {info}"))
    pass


def set_root_export():
    working_dir = os.getcwd()
    execute_os_cmd("Setting up root export for PWNBOX using this directory.", f"echo \"export PWNBOX_ROOT=\"" + working_dir + " > /etc/profile.d/pwnbox_setup.sh && chmod +x /etc/profile.d/pwnbox_setup.sh")
    pass


def set_default_config():
    execute_os_cmd("Setting up config directory in /etc/ for PWNBOX as /etc/pwnbox.", "mkdir -p /etc/pwnbox/")
    execute_os_cmd("Creating default .ini file for later use. This file will hold persistent settings as to what to load on boot.", "touch /etc/pwnbox/pwncfg.ini")

    config = configparser.ConfigParser()
    config.read('/etc/pwnbox/pwncfg.ini')

    f = open('./default_config.json')
    data = json.load(f)

    for col in data:
        for opt in col.collection:
            config[f'{ col.name }'][f'{ opt }']=False

    with open('/etc/pwnbox/pwncfg.ini', 'w') as configfile:
        config.write(configfile)

    pass


def bypass_rc_local():
    with open('/etc/rc.local', 'r') as file :
        filedata = file.read()
    filedata = filedata.replace('exit 0', "$PWNBOX_ROOT/load_hid_kernel.sh\r\nexit 0")
    with open('/etc/rc.local', 'w') as file:
        file.write(filedata)
    pass


def main():
    set_root_export()
    set_default_config()
    bypass_rc_local()
    pass


if __name__ == "__init__":
    main()