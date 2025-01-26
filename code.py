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

import adafruit_ov5640
import adafruit_veml7700
import adafruit_bh1750
import supervisor

# can try import bitmap_label below for alternative
from adafruit_display_text import label
import adafruit_displayio_sh1107

displayio.release_displays()
# oled_reset = board.D9

dir(board)

print(f"Run reason: {supervisor.runtime.run_reason}")

#== Connect to camera

print("construct camera")

# Camera is on I2C0
cam_i2c = board.STEMMA_I2C()
#cam_i2c = busio.I2C(board.GP5, board.GP4)

reset = digitalio.DigitalInOut(board.GP14)
cam = adafruit_ov5640.OV5640(
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
    reset=reset,
    size=adafruit_ov5640.OV5640_SIZE_240X240,
)
print(f"chip id: {cam.chip_id}")

veml7700 = adafruit_veml7700.VEML7700(cam_i2c)
bh1750 = adafruit_bh1750.BH1750(cam_i2c)


# Set up I2C1 for display
print("Initializing display")
display_i2c = busio.I2C(board.GP19, board.GP18)
display_bus = I2CDisplayBus(display_i2c, device_address=0x3C)

# SH1107 is vertically oriented 64x128
WIDTH = 128
HEIGHT = 64
BORDER = 2

display = adafruit_displayio_sh1107.SH1107(display_bus, width=WIDTH, height=HEIGHT)

# Make the display context
splash = displayio.Group()
display.root_group = splash

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
dy = 24

dummy_text = "0123456789ABCDEFG"  # overly long to see where it clips

line1 = label.Label(terminalio.FONT, text=dummy_text, scale=1, color=0xFFFFFF, x=x_offset, y=y_offset)
splash.append(line1)

line2 = label.Label(
    terminalio.FONT, text=dummy_text, scale=1, color=0xFFFFFF, x=x_offset, y=y_offset+dy
)
splash.append(line2)

line3 = label.Label(
    terminalio.FONT, text=dummy_text, scale=1, color=0xFFFFFF, x=x_offset, y=y_offset+2*dy
)
splash.append(line3)

count = 0

iso = 400

while True:

    lux = bh1750.lux
    ev = math.log(lux * 0.4)

    lux2 = veml7700.lux

    line1.text = f"f/{count}"
    line2.text = f"L: {lux:.2f}"
    line3.text = f"L: {lux2:.2f}"

    time.sleep(0.5)   

