import os
import configparser

default_config = {
    {
        "name": "TYPES",
        "collection": [
            "KEYBOARD"
        ]
    }
}

def set_root_export():
    os.system(f"echo \"export PWNBOX_ROOT={os.getcwd()}\" > /etc/profile.d/pwnbox_setup.sh")
    pass


def set_default_config():
    os.system('mkdir -p /etc/pwnbox/ && touch /etc/pwnbox/pwncfg.ini')

    config = configparser.ConfigParser()
    config.read('/etc/pwnbox/pwncfg.ini')

    for col in default_config:
        for opt in col.collection:
            config[f'{ col.name }'][f'{ opt }']=False

    with open('/etc/pwnbox/pwncfg.ini', 'w') as configfile:
        config.write(configfile)

    pass


def main():
    set_root_export()
    set_default_config()
    pass


if __name__ == "__init__":
    main()