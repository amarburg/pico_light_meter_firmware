# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
Author: Mark Roberts (mdroberts1243) from Adafruit code
This test will initialize the display using displayio and draw a solid white
background, a smaller black rectangle, miscellaneous stuff and some white text.

"""


import board
import digitalio
import busio
import displayio
from displayio import I2CDisplay as I2CDisplayBus
import terminalio
import time
import math
import sys

# Sensors connected via Stemma
import adafruit_ov5640
import adafruit_veml7700
import adafruit_bh1750
import supervisor

# can try import bitmap_label below for alternative
from adafruit_display_text import label
from adafruit_displayio_sh1107 import SH1107
from fourwire import FourWire
from adafruit_st7789 import ST7789


#== Connect to camera

class Camera:

    def __init__(self, cam_i2c, bitmap=None):
        # Camera is on I2C0

        self.size=adafruit_ov5640.OV5640_SIZE_QVGA #320x240

        self.reset = digitalio.DigitalInOut(board.GP14)
        self.cam = adafruit_ov5640.OV5640(
            cam_i2c,
            data_pins=(
                board.GP6,
                board.GP7,
                board.GP8,
                board.GP9,
                board.GP10,
                board.GP11,
                board.GP12,
                board.GP13,
            ),
            clock=board.GP3,
            vsync=board.GP0,
            href=board.GP2,
            mclk=None,
            shutdown=None,
            reset=self.reset,
            size=self.size, 
        )
        print(f"chip id: {self.cam.chip_id}")

        self.cam.colorspace = adafruit_ov5640.OV5640_COLOR_RGB
        self.cam.flip_y = True
        self.cam.flip_x = False
        self.cam.test_pattern = False

        if bitmap:
            self.buf = bitmap
        else:
            self.buf = bytearray(self.cam.capture_buffer_size)

        # chars = b" .':-+=*%$#"
        # remap = [chars[i * (len(chars) - 1) // 255] for i in range(256)]

        # width = self.cam.width
        # row = bytearray(width)

    def capture(self):
        self.cam.capture(self.buf)
        return self.buf

