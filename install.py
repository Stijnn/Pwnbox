import os

os.system(f"echo \"export PWNBOX_ROOT={os.getcwd()}\" > /etc/profile.d/pwnbox_setup.sh")