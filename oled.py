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


class OledDisplay:

    def __init__(self):

        # Set up I2C1 for display
        print("Initializing display")
        oled_display_i2c = busio.I2C(board.GP27, board.GP26)
        oled_display_bus = I2CDisplayBus(oled_display_i2c, device_address=0x3C)

        # SH1107 is vertically oriented 64x128
        WIDTH = 128
        HEIGHT = 64
        BORDER = 2

        self.oled_display = SH1107(oled_display_bus, width=WIDTH, height=HEIGHT)

        # Make the display context
        self.splash = displayio.Group()
        self.oled_display.root_group = splash

        # color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
        # color_palette = displayio.Palette(1)
        # color_palette[0] = 0xFFFFFF  # White

        # bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        # splash.append(bg_sprite)

        # Draw a smaller inner rectangle in black
        # inner_bitmap = displayio.Bitmap(WIDTH - BORDER * 2, HEIGHT - BORDER * 2, 1)
        # inner_palette = displayio.Palette(1)
        # inner_palette[0] = 0x000000  # Black
        # inner_sprite = displayio.TileGrid(
        #     inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
        # )
        # splash.append(inner_sprite)

        # Draw some white squares
        # sm_bitmap = displayio.Bitmap(8, 8, 1)
        # sm_square = displayio.TileGrid(sm_bitmap, pixel_shader=color_palette, x=58, y=17)
        # splash.append(sm_square)

        # med_bitmap = displayio.Bitmap(16, 16, 1)
        # med_square = displayio.TileGrid(med_bitmap, pixel_shader=color_palette, x=71, y=15)
        # splash.append(med_square)

        # lrg_bitmap = displayio.Bitmap(32, 32, 1)
        # lrg_square = displayio.TileGrid(lrg_bitmap, pixel_shader=color_palette, x=91, y=28)
        # splash.append(lrg_square)

        # Draw some label text
        y_offset = 8
        x_offset = 4
        dy = 12

        dummy_text = "0123456789ABCDEFG"  # overly long to see where it clips

        self.line1 = label.Label(terminalio.FONT, text=dummy_text, scale=1, color=0xFFFFFF, x=x_offset, y=y_offset)
        splash.append(line1)

        self.line2 = label.Label(
            terminalio.FONT, text=dummy_text, scale=1, color=0xFFFFFF, x=x_offset, y=y_offset+dy
        )
        self.splash.append(line2)

        self.line3 = label.Label(
            terminalio.FONT, text=dummy_text, scale=1, color=0xFFFFFF, x=x_offset, y=y_offset+2*dy
        )
        self.splash.append(line3)

        self.line4 = label.Label(
            terminalio.FONT, text=dummy_text, scale=1, color=0xFFFFFF, x=x_offset, y=y_offset+3*dy
        )
        self.splash.append(line4)

        self.line5 = label.Label(
            terminalio.FONT, text=dummy_text, scale=1, color=0xFFFFFF, x=x_offset, y=y_offset+4*dy
        )
        self.splash.append(line5)
