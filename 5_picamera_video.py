#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Reference: https://github.com/rm-hull/luma.examples

import io
import sys
import time
import threading
from PIL import Image
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106

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


# create a pool of image processors
done = False
lock = threading.Lock()
pool = []

class ImageProcessor(threading.Thread):
    def __init__(self):
        super(ImageProcessor, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.start()

    def run(self):
        # this method runs in a separate thread
        global done
        while not self.terminated:
            # wait for an image to be written to the stream
            if self.event.wait(1):
                try:
                    self.stream.seek(0)

                    # read the image and display it on screen
                    photo = Image.open(self.stream)
                    device.display(photo.convert(device.mode))

                    # set done to True if you want the script to terminate
                    # at some point
                    # done=True
                finally:
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()

                    # return ourselves to the pool
                    with lock:
                        pool.append(self)

def streams():
    while not done:
        with lock:
            if pool:
                processor = pool.pop()
            else:
                processor = None
        if processor:
            yield processor.stream
            processor.event.set()
        else:
            # when the pool is starved, wait a while for it to refill
            time.sleep(0.1)

cameraResolution = (640, 480)
cameraFrameRate = 8

with picamera.PiCamera() as camera:
    pool = [ImageProcessor() for i in range(4)]

    # set camera resolution
    camera.resolution = cameraResolution
    camera.framerate = cameraFrameRate

    print("Starting camera preview...")
    camera.start_preview()
    time.sleep(2)

    print("Capturing video...")
    try:
        camera.capture_sequence(streams(), use_video_port=True, resize=device.size)

        # shut down the processors in an orderly fashion
        while pool:
            with lock:
                processor = pool.pop()
            processor.terminated = True
            processor.join()
    except KeyboardInterrupt:
        pass
