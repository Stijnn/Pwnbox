from genericpath import exists
import os
from termcolor import colored

LOG_FILE_PATH:str = None

def set_log_file(log_file: str = None):
    LOG_FILE_PATH = log_file


def __log__(code, color, text: str):
    print(f'[ {colored(code, color)} ] {text}')
    
    if LOG_FILE_PATH == None:
        return

    if not exists(LOG_FILE_PATH):
        log_command(f'touch {LOG_FILE_PATH}')
        log_command(f'chmod +rw {LOG_FILE_PATH}')

    if exists(LOG_FILE_PATH):
        f = open(LOG_FILE_PATH, 'w+')
        if f:
            f.write(f'[ {colored(code, color)} ] {text}\n')


def log_command(command: str) -> int:
    exit_code = os.system(command)
    log_ok(command) if exit_code == 0 else log_error(command)
    return exit_code


def log_ok(text: str):
    __log__('OK', 'green', text)


def log_error(text: str):
    __log__('ERR', 'red', text)


def log_warning(text: str):
    __log__('WRN', 'yellow', text)


def log_verbose(text: str):
    __log__('VRB', 'cyan', text)