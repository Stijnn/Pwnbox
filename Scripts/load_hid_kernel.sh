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

echo "Pwnbox Developer" > strings/0x409/manufacturer
echo "Pwnbox Gadget Box" > strings/0x409/product

mkdir -p configs/c.1/strings/0x409

cd $1
python $1/boot_script.py /sys/kernel/config/usb_gadget/pwnbox_kernel

cd /sys/kernel/config/usb_gadget/pwnbox_kernel
ls /sys/class/udc > UDC