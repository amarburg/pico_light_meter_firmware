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

# can try import bitmap_label below for alternative
from fourwire import FourWire
from adafruit_st7789 import ST7789

import adafruit_ov5640


class TftDisplay:

    def __init__(self, spi, cam_size):

        tft_cs = board.GP21
        tft_dc = board.GP20
        tft_display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs)
        self.display = ST7789(tft_display_bus, height=320, width=240 )
        self.display.root_group = None
        self.display.rotation=90

        if cam_size == adafruit_ov5640.OV5640_SIZE_QVGA:
            self.width = 320
            self.height = 240
            x_offset=0
            y_offset=0
        else:
            raise "Unknown image size"
        
        self.bitmap = displayio.Bitmap(self.width, self.height, 65535)
        
        if self.bitmap is None:
            raise SystemExit("Could not allocate a bitmap")

        g = displayio.Group(scale=1, x=x_offset, y=y_offset)
        tg = displayio.TileGrid(self.bitmap,
            pixel_shader=displayio.ColorConverter(input_colorspace=displayio.Colorspace.RGB565_SWAPPED)
        )
        g.append(tg)
        self.display.root_group = g
    
    def refresh(self,**args):
        self.display.refresh(**args)