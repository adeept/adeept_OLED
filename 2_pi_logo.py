#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Reference: https://github.com/rm-hull/luma.examples

from pathlib import Path
from PIL import Image

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
import time
import threading

try:
    serial = i2c(port=1, address=0x3C)  # Set the I2C address of the OLED
    device = ssd1306(serial, rotate=0)
except:
    print('OLED disconnected')

def main():
    img_path = str(Path(__file__).resolve().parent.joinpath('images', 'pi_logo.png'))
    logo = Image.open(img_path).convert("RGBA")
    fff = Image.new(logo.mode, logo.size, (255,) * 4)

    background = Image.new("RGBA", device.size, "white")
    posn = ((device.width - logo.width) // 2, 0)

    while True:
        for angle in range(0, 360, 2):
            rot = logo.rotate(angle, resample=Image.BILINEAR)
            img = Image.composite(rot, fff, rot)
            background.paste(img, posn)
            device.display(background.convert(device.mode))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
