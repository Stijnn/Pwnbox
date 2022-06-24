import configparser
import argparse

from genericpath import exists
import os
import logging
import queue
import sys

import subprocess

import datetime
from time import sleep
from pwnboxlib.cdc_ecm.cdc_ecm import EthernetFactory
from pwnboxlib.mouse.mouse import MouseFactory

from pwnboxlib.devicefactory import DeviceFactory
from pwnboxlib.keyboard.keyboard import KeyboardFactory
from pwnboxlib.mass_storage.mass_storage import StorageFactory
from pwnboxlib.rndis.rndis import RNDISFactory

from pwnlogger import log_command, log_error, log_ok, log_verbose, log_warning, set_log_file


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
        'proxy_type': KeyboardFactory('hid.usb0'),
        'add_to_tmp': True,
        'tmp_name': 'keyboard'
    },
    'STORAGE': { 
        'should_enable': config.getboolean('TYPES', 'STORAGE'),
        'proxy_type': StorageFactory('mass_storage.usb0', f'{PWNBOX_PATH}/diskimage.img'),
        'add_to_tmp': False
    },
    'CDC_ECM': { 
        'should_enable': config.getboolean('TYPES', 'CDC_ECM'),
        'proxy_type': EthernetFactory('ecm.usb0'),
        'add_to_tmp': False,
        'ip': '192.168.4.1',
        'netmask': '255.255.255.0'
    },
    'RNDIS': { 
        'should_enable': config.getboolean('TYPES', 'RNDIS'),
        'proxy_type': RNDISFactory('rndis.usb0'),
        'add_to_tmp': False,
        'ip': '192.168.4.1',
        'netmask': '255.255.255.0'
    },
    'MOUSE': { 
        'should_enable': config.getboolean('TYPES', 'MOUSE'),
        'proxy_type': MouseFactory('hid.usb1'),
        'add_to_tmp': True,
        'tmp_name': 'mouse'
    }
})


def start_load(device: DeviceFactory):
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
    log_command('mkdir -p /tmp/pwnbox/')

    loaded_devices = []
    for k,v in DEVICE_CONFIG.items():
        if not v.__contains__('should_enable'):
            continue

        if not v['should_enable']:
            continue

        if chdir_gadget():
            if isinstance(v['proxy_type'], DeviceFactory):
                log_ok(f'Loading: {k} with Proxy({ type(v["proxy_type"]) }) named {v["proxy_type"].device_name}')
                start_load(v['proxy_type'])
                loaded_devices.append(v)

    chdir_pwnbox()
    return loaded_devices


def disable_udc():
    if chdir_gadget():
        log_command('echo "" > UDC')
        chdir_pwnbox()
        log_ok('Succesfully disabled gadget...')
    else:
        log_warning('Device does not exists. Skipping disabling...')
    pass


def load_gadget():
    if exists(GADGET_PATH):
        log_warning('Gadget already exists. Skipping load...')
        return

    log_verbose(f'Creating {GADGET_PATH}')
    log_command(f'mkdir -p {GADGET_PATH}')
    if chdir_gadget():
        for k,v in GADGET_CONFIG.items():
            log_verbose(f'echo {v} > {k}')
            log_command(f'echo {v} > {k}')

        for k, v in STRINGS_CONFIG.items():
            log_command(f'mkdir -p strings/{k}')
            log_command(f'echo {v["serialnumber"]} > strings/{k}/serialnumber')
            log_command(f'echo {v["manufacturer"]} > strings/{k}/manufacturer')
            log_command(f'echo {v["product"]} > strings/{k}/product')
            pass

        log_command(f'mkdir -p configs/c.1/strings/0x409')
        log_command('echo "Config 1: RNDIS network" > configs/c.1/strings/0x409/configuration')
        log_command('echo 250 > configs/c.1/MaxPower')
        log_command('echo 0x80 > configs/c.1/bmAttributes')

        chdir_pwnbox()
        loaded_devices = on_post_device_creation()

        if chdir_gadget():
            log_command('ls /sys/class/udc > UDC')

        if loaded_devices != None:
            for dev in loaded_devices:
                if dev["add_to_tmp"]:
                    dev_path = f"/configs/c.1/{dev['proxy_type'].device_name}/dev"
                    log_command(f'udevadm info -rq name  /sys/dev/char/$(cat {GADGET_PATH + dev_path}) > /tmp/pwnbox/{dev["tmp_name"]}')
                    with open(f'/tmp/pwnbox/{dev["tmp_name"]}', 'r') as link_file:
                        log_command(f'chmod 777 {link_file.readline().strip()}')
                        

        chdir_pwnbox()
        log_ok('Succesfully loaded gadget...')

    if DEVICE_CONFIG['CDC_ECM']['should_enable']:
        log_command(f'ifconfig usb0 {DEVICE_CONFIG["CDC_ECM"]["ip"]} netmask {DEVICE_CONFIG["CDC_ECM"]["netmask"]} up')


    if DEVICE_CONFIG['RNDIS']['should_enable']:
        log_command(f'ifconfig usb0 {DEVICE_CONFIG["RNDIS"]["ip"]} netmask {DEVICE_CONFIG["RNDIS"]["netmask"]} up')

        
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
                    log_command(f'rm -rf {path}/{file}')

                for dir in subdirs:
                    filo_paths.put(path +'/'+ dir)
            
            while not filo_paths.empty():
                path = filo_paths.get()
                log_warning(f'Removing: {path}')
                log_command(f'rm -f {path}')
                log_command(f'rmdir {path}')

        log_warning(f'Removing: {GADGET_PATH}')
        os.rmdir(GADGET_PATH)
        chdir_pwnbox()

        log_command('rm -rf /tmp/pwnbox/*')

        if not os.path.exists(GADGET_PATH):
            log_ok('Succesfully unloaded gadget...')
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
parser.add_argument('--no-logging', action='store_true', help='Do not create a logfile')

# 

args = parser.parse_args()


def main():
    if not is_root():
        log_error('This program requires root privilages to run. Please use sudo.')
        return

    print('\r\n\r\n')
    [print(x.replace('\n', '')) for x in open(f'{PWNBOX_PATH}/banner.txt', 'r').readlines()]
    print('\r\n\r\n')

    #if not args['no-logging']:
    log_command(f'mkdir -p {PWNBOX_PATH}/logs/')
    set_log_file(f'{PWNBOX_PATH}/logs/log_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}')

    if args.load:       load_gadget()
    if args.disable:    disable_udc()
    if args.unload:     unload_gadget()
    pass


if __name__ == "__main__":
    main()