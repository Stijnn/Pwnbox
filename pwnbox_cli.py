import configparser
import argparse

from genericpath import exists
import os
import logging
import queue
import sys

import subprocess

from datetime import datetime
from time import sleep

from pwnboxlib.proxydevice import ProxyDevice
from pwnlogger import log_error, log_verbose, log_warning, log


USB_GADGET_NAME = "pwnbox_gadget"
PWNBOX_CONFIG = '/etc/pwnbox/pwncfg.ini'
GADGET_PATH = f'/sys/kernel/config/usb_gadget/{USB_GADGET_NAME}'
PWNBOX_PATH =  os.path.abspath(os.path.dirname(sys.argv[0]))

config = configparser.ConfigParser()
config.read(PWNBOX_CONFIG)

GADGET_CONFIG = dict({
    'idVendor'  : 0x1d6b,
    'idProduct' : 0x0104,
    'bcdDevice' : 0x0100,    
    'bcdUSB'    : 0x0200,
})


STRINGS_CONFIG = dict({
    '0x409': {
        'serialnumber': "0xdeadbeef420024",
        'manufacturer': "Pwnbox Developer",
        'product': "Pwnbox Gadget Box"
    }
})


DEVICE_CONFIG = dict({
    'KEYBOARD': { 
        'should_enable': config.getboolean('TYPES', 'KEYBOARD'),
        'proxy_type': ProxyDevice('hid.usb0')
    },
    'KEYBOARD': { 
        'should_enable': config.getboolean('TYPES', 'STORAGE'),
        'proxy_type': ProxyDevice('mass_storage.usb0')
    }
})


def start_load(device: ProxyDevice):
    device.build()
    pass


def chdir_gadget():
    if exists(GADGET_PATH):
        os.chdir(GADGET_PATH)
        return True
    else:
        return False


def chdir_pwnbox():
    os.chdir(PWNBOX_PATH)


def on_post_device_creation():
    for k,v in DEVICE_CONFIG.items():
        if not v.__contains__('should_enable'):
            continue

        if chdir_gadget():
            if isinstance(v['proxy_type'], ProxyDevice):
                start_load(v['proxy_type'])

    chdir_pwnbox()
    pass


def disable_udc():
    if chdir_gadget():
        os.system('echo "" > UDC')
        chdir_pwnbox()
        log('Succesfully disabled gadget...')
    else:
        log_warning('Device does not exists. Skipping disabling...')
    pass


def load_gadget():
    if exists(GADGET_PATH):
        log_warning('Gadget already exists. Skipping load...')
        return

    log_verbose(f'Creating {GADGET_PATH}')
    os.system(f'mkdir -p {GADGET_PATH}')
    if chdir_gadget():
        for k,v in GADGET_CONFIG.items():
            log_verbose(f'echo {v} > {k}')
            os.system(f'echo {v} > {k}')

        for k, v in STRINGS_CONFIG.items():
            os.system(f'mkdir -p strings/{k}')
            os.system(f'echo {v["serialnumber"]} > strings/{k}/serialnumber')
            os.system(f'echo {v["manufacturer"]} > strings/{k}/manufacturer')
            os.system(f'echo {v["product"]} > strings/{k}/product')
            pass

        os.system(f'mkdir -p configs/c.1/strings/0x409')
        os.system('echo "Config 1: RNDIS network" > configs/c.1/strings/0x409/configuration')
        os.system('echo 250 > configs/c.1/MaxPower')
        os.system('echo 0x80 > configs/c.1/bmAttributes')

        chdir_pwnbox()
        on_post_device_creation()

        if chdir_gadget():
            os.system('ls /sys/class/udc > UDC')

        chdir_pwnbox()
        log('Succesfully loaded gadget...')
    pass


def unload_gadget():
    if chdir_gadget():
        disable_udc()

        first_in_order = ['configs', 'functions', 'strings']
        for d in first_in_order:
            filo_paths = queue.LifoQueue()
            for path, subdirs, files in os.walk(f'{GADGET_PATH}/{d}'):
                for file in files:
                    log_warning(f'Removing: {file}')
                    log_verbose(os.system(f'rm -rf {path}/{file}'))

                for dir in subdirs:
                    filo_paths.put(path +'/'+ dir)
            
            while not filo_paths.empty():
                path = filo_paths.get()
                log_warning(f'Removing: {path}')
                log_verbose(os.system(f'rm -f {path}'))
                log_verbose(os.system(f'rmdir {path}'))

        log_warning(f'Removing: {GADGET_PATH}')
        os.rmdir(GADGET_PATH)
        chdir_pwnbox()

        if not os.path.exists(GADGET_PATH):
            log('Succesfully unloaded gadget...')
        else:
            log_error(f'Could not fully remove {GADGET_PATH}')
    else:
        log_warning('Gadget has not yet been loaded. Skipping unload...')
    pass


def is_root():
    return os.geteuid() == 0


##############################################
#
#   Entry point with argument parsing
#
##############################################

parser = argparse.ArgumentParser(description='Pwnbox Command Line Interface Utility Program')

# Loading/Unloading
parser.add_argument('--load', action='store_true', help='Load gadget if unloaded.')
parser.add_argument('--unload', action='store_true', help='Unload gadget if loaded.')
parser.add_argument('--disable', action='store_true', help='Disable the gadget but dont unload')

# 

args = parser.parse_args()


def main():
    if not is_root():
        log_error('This program requires root privilages to run. Please use sudo.')
        return

    print('\r\n\r\n')
    [print(x) for x in open(f'{PWNBOX_PATH}/banner.txt', 'r').readlines()]
    print('\r\n\r\n')

    if args.load:       load_gadget()
    if args.disable:    disable_udc()
    if args.unload:     unload_gadget()
    pass


if __name__ == "__main__":
    main()