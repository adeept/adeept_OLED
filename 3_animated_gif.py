#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Reference: https://github.com/rm-hull/luma.examples

from pathlib import Path
from PIL import Image, ImageSequence
from luma.core.sprite_system import framerate_regulator

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106

try:
    serial = i2c(port=1, address=0x3C)  # Set the I2C address of the OLED
    device = ssd1306(serial, rotate=0)
except:
    print('OLED disconnected')

def run():
    regulator = framerate_regulator(fps=10)
    img_path = str(Path(__file__).resolve().parent.joinpath('images', 'banana.gif'))
    banana = Image.open(img_path)
    size = [min(*device.size)] * 2
    posn = ((device.width - size[0]) // 2, device.height - size[1])

    while True:
        for frame in ImageSequence.Iterator(banana):
            with regulator:
                background = Image.new("RGB", device.size, "white")
                background.paste(frame.resize(size, resample=Image.LANCZOS), posn)
                device.display(background.convert(device.mode))


if __name__ == "__main__":
    try:
        print('Press "Ctrl + C" to stop the program.')
        run()
    except KeyboardInterrupt:
        pass
