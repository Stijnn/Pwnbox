#!/bin/bash

cd /sys/kernel/config/usb_gadget/

mkdir -p pwnbox_kernel
cd pwnbox_kernel

echo 0x1d6b > idVendor # Linux Foundation
echo 0x0104 > idProduct # Multifunction Composite Gadget
echo 0x0100 > bcdDevice # v1.0.0
echo 0x0200 > bcdUSB # USB2

mkdir -p strings/0x409

echo "0xdeadbeef420024" > strings/0x409/serialnumber

echo "Stijn Verhelpen" > strings/0x409/manufacturer
echo "Pwnbox Gadget Box" > strings/0x409/product

mkdir -p configs/c.1/strings/0x409

echo "Config 1: ECM network" > configs/c.1/strings/0x409/configuration
echo 250 > configs/c.1/MaxPower
# Add functions here

python $(PWNBOX_ROOT)/boot_script.py

# End functions
ls /sys/class/udc > UDC