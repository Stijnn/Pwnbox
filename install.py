import os
import configparser
import sys

from termcolor import colored
from genericpath import exists

#
#   CONFIG PATHS
#

PWN_CONFIG_FILE_PATH = '/etc/pwnbox/pwncfg.ini'

PWN_ROOT = os.path.abspath(os.path.dirname(sys.argv[0]))
PWN_BOOT_SHELL_SCRIPT_FILE_PATH = 'python3 ' + PWN_ROOT + '/pwnbox_cli.py --load '

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
        "KEYBOARD": False,
        "STORAGE": False,
        "CDC_ECM": False,
        "RNDIS": False,
        "MOUSE": False
    }

    with open(PWN_CONFIG_FILE_PATH, 'w') as configfile:
        config.write(configfile)

    pass


def bypass_rc_local():
    with open(RC_LOCAL_FILE_PATH, 'r') as file :
        filedata = file.readlines()

    new_lines = []
    check_hit = False
    # Prevent duplicate writes
    for line in filedata:
        if line.startswith('#'):
            new_lines.append(line)
            continue
        elif line.__contains__(PWN_BOOT_SHELL_SCRIPT_FILE_PATH):
            print(colored(f"[~] Bypass to {PWN_BOOT_SHELL_SCRIPT_FILE_PATH} already exists. Skipping creation...", "yellow"))
            check_hit = True
            new_lines.append(line)
            continue
        elif line.__contains__("exit 0"):
            if not check_hit:
                print(colored(f"[#] Bypass to {PWN_BOOT_SHELL_SCRIPT_FILE_PATH} created. Now writing changes...", "green"))
                check_hit = True
                new_lines.append(line.replace('exit 0', PWN_BOOT_SHELL_SCRIPT_FILE_PATH + '\r\nexit 0'))
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    
    with open(RC_LOCAL_FILE_PATH, 'w') as file:
        file.writelines(new_lines)
        
    pass


def create_mass_storage_image():
    image_location = f'{PWN_ROOT}/diskimage.img'
    print(f'Image location {image_location}')
    if not exists(image_location):
        if execute_os_cmd('Creating image using DD...', f'dd if=/dev/zero of={image_location} count=1024 bs=1M') == 0:
            execute_os_cmd('Making FAT32 MS-DOS FileSystem...', f'mkdosfs {image_location}')
    pass


def main():
    set_default_config()
    bypass_rc_local()

    create_mass_storage_image()

    execute_os_cmd('Enable USB Kernel', 'echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt')
    execute_os_cmd('Enable USB Kernel', 'echo "dwc2" | sudo tee -a /etc/modules')
    execute_os_cmd('Enable USB Kernel', 'sudo echo "libcomposite" | sudo tee -a /etc/modules')
    execute_os_cmd('Enable USB Module', 'echo "g_multi" | sudo tee -a /etc/modules')

    execute_os_cmd('Update system', 'sudo apt -y update && sudo apt -y upgrade')

    pass


if __name__ == "__main__":
    main()