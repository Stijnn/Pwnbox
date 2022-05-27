import os
import configparser
from termcolor import colored
from genericpath import exists

def execute_os_cmd(info: str, command: str) -> int:
    exit_code = os.system(command)
    print(colored(f"[{exit_code}] Error: {info}", 'red') if exit_code != 0 else colored(f"[#] Succes: {info}", 'green'))
    return exit_code


def set_root_export():
    working_dir = os.getcwd()
    
    file_exists = exists('/etc/profile.d/pwnbox_setup.sh')
    if not file_exists:
        success = execute_os_cmd(
            "Setting up root export for PWNBOX using this directory.", 
            f"echo \"#!/bin/bash\r\nexport $PWNBOX_ROOT=\"" + working_dir + " > /etc/profile.d/pwnbox_setup.sh && chmod +x /etc/profile.d/pwnbox_setup.sh"
        ) == 0

        if success:
            execute_os_cmd(
                "Sourcing file to set PWNBOX_ROOT for use in shell scripts downstream install",
                "source /etc/profile.d/pwnbox_setup.sh"
            )
    else:
        print(colored("[~] Warning: /etc/profile.d/pwnbox_setup.sh already exists. Skipping Creation...", 'yellow'))
    pass


def set_default_config():

    execute_os_cmd(
        "Setting up config directory in /etc/ for PWNBOX as /etc/pwnbox.", 
        "mkdir -p /etc/pwnbox/"
    )

    execute_os_cmd(
        "Creating default .ini file for later use. This file will hold persistent settings as to what to load on boot.", 
        "touch /etc/pwnbox/pwncfg.ini"
    )

    config = configparser.ConfigParser()
    config.read('/etc/pwnbox/pwncfg.ini')

    config["TYPES"] = {
        "KEYBOARD": False
    }

    with open('/etc/pwnbox/pwncfg.ini', 'w') as configfile:
        config.write(configfile)

    pass


def bypass_rc_local():
    with open('/etc/rc.local', 'r') as file :
        filedata = file.read()

    # Prevent duplicate writes
    if not filedata.__contains__('$PWNBOX_ROOT/load_hid_kernel.sh'):
        filedata = filedata.replace('exit 0', "$PWNBOX_ROOT/load_hid_kernel.sh\r\nexit 0")
        with open('/etc/rc.local', 'w') as file:
            file.write(filedata)
    pass


def main():
    set_root_export()
    set_default_config()
    bypass_rc_local()
    pass


if __name__ == "__main__":
    main()