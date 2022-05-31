import os
from termcolor import colored


def __log__(chr, clr, txt, type):
    print(colored(f'[{chr}]{type}:{os.getuid()}:{txt}', f'{clr}'))


def log(text: str):
    __log__('#', 'green', text, 'INFO')
    pass


def log_error(text: str):
    __log__('!', 'red', text, 'ERROR')
    pass


def log_warning(text: str):
    __log__('~', 'yellow', text, 'WARNING')
    pass


def log_verbose(text: str):
    __log__('@', 'blue', text, 'VERBOSE')
    pass