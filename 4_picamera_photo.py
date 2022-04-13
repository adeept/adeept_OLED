#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Reference: https://github.com/rm-hull/luma.examples

import io
import sys
import time
from PIL import Image
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106

try:
    serial = i2c(port=1, address=0x3C)  # Set the I2C address of the OLED
    device = ssd1306(serial, rotate=0)
except:
    print('OLED disconnected')

# from demo_opts import get_device

try:
    serial = i2c(port=1, address=0x3C)  # Set the I2C address of the OLED
    device = ssd1306(serial, rotate=0)
except:
    print('OLED disconnected')

try:
    import picamera
except ImportError:
    print("The picamera library is not installed. Install it using 'sudo -H pip install picamera'.")
    sys.exit()


def run():
    cameraResolution = (1024, 768)
    displayTime = 5

    # create the in-memory stream
    stream = io.BytesIO()
    with picamera.PiCamera() as camera:
        # set camera resolution
        camera.resolution = cameraResolution

        print("Starting camera preview...")
        camera.start_preview()
        time.sleep(2)

        print("Capturing photo...")
        camera.capture(stream, format='jpeg', resize=device.size)

        print("Stopping camera preview...")
        camera.close()

        # "rewind" the stream to the beginning so we can read its content
        stream.seek(0)

        print("Displaying photo for {0} seconds...".format(displayTime))

        # open photo
        photo = Image.open(stream)

        # display on screen for a few seconds
        device.display(photo.convert(device.mode))
        time.sleep(displayTime)

        print("Done.")


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        pass
