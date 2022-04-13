#!/usr/bin/env/python3
# Description : for OLED functions

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
import time

try:
    serial = i2c(port=1, address=0x3C)  # Set the I2C address of the OLED
    device = ssd1306(serial, rotate=0)
except:
    print('OLED disconnected')

'''
 -------- X
|
|
|
Y
'''
text_1 = 'Hello'
text_2 = '    World!'
text_3 = '     OLED Module   '
text_4 = ' '
text_5 = '       by adeept.com'


def run():
    with canvas(device) as draw:
        draw.text((0, 0), text_1, fill="white")     # (0, 0): (x,y)the starting position of the text display.
        draw.text((0, 10), text_2, fill="white")    # text_2: text content.
        draw.text((0, 20), text_3, fill="white")
        draw.text((0, 30), text_4, fill="white")
        draw.text((0, 40), text_5, fill="white")

if __name__ == '__main__':
    run()               #
    while True:         # To keep the program running.
        time.sleep(10)  # Terminate the program by pressing the keys "Ctrl + C".