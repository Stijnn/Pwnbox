#!/bin/bash

CONFIG_INDEX = $1

mkdir -p functions/hid.usb$1
echo 1 > functions/hid.usb$1/protocol
echo 1 > functions/hid.usb$1/subclass
echo 8 > functions/hid.usb$1/report_length
echo -ne \\x05\\x01\\x09\\x06\\xa1\\x01\\x05\\x07\\x19\\xe0\\x29\\xe7\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x08\\x81\\x02\\x95\\x01\\x75\\x08\\x81\\x03\\x95\\x05\\x75\\x01\\x05\\x08\\x19\\x01\\x29\\x05\\x91\\x02\\x95\\x01\\x75\\x03\\x91\\x03\\x95\\x06\\x75\\x08\\x15\\x00\\x25\\x65\\x05\\x07\\x19\\x00\\x29\\x65\\x81\\x00\\xc0 > functions/hid.usb$1/report_desc

echo "Config ${CONFIG_INDEX}: ECM network" > configs/c.1/strings/0x409/configuration
echo 250 > configs/c.1/MaxPower

ln -s functions/hid.usb$1 configs/c.1/

exit 0