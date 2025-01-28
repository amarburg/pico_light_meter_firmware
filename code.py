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

import adafruit_ov5640
import adafruit_veml7700
import adafruit_bh1750
import supervisor

# can try import bitmap_label below for alternative
from adafruit_display_text import label
import adafruit_displayio_sh1107

POS_SHUTTER_SPEEDS = [
    1, 2 ,4 ,8, 15, 30, 60, 125, 250, 500, 1000
]
NEG_SHUTTER_SPEEDS = [
    1, "2s", "4s", "8s", "15s", "30s", "60s", "2m", "4m", "8m"
]

APERTURE_EV = ["1.0", "1.4", "2.0", "2.8", "4.0", "5.6", "8.0", "11", "16", "22", "32"]

def ev_to_shutter_speed( ev ):

    rev = round(abs(ev))

    if rev == 0:
        return "1"
    elif ev > 0:
        if rev >= len(POS_SHUTTER_SPEEDS):
            return "MIN"
        else:
            return f"1/{POS_SHUTTER_SPEEDS[rev]}"

    else:
        if rev >= len(NEG_SHUTTER_SPEEDS):
            return "LONG"
        else:
            return NEG_SHUTTER_SPEEDS[rev]

    if ev >= 0:
        return f"1/{ss}"
    else:
        return f"{ss}s"



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
    size=adafruit_ov5640.OV5640_SIZE_QVGA, #320x240
)
print(f"chip id: {cam.chip_id}")

cam.colorspace = adafruit_ov5640.OV5640_COLOR_RGB
cam.flip_y = False
cam.flip_x = False
cam.test_pattern = False


buf = bytearray(cam.capture_buffer_size)
chars = b" .':-+=*%$#"
remap = [chars[i * (len(chars) - 1) // 255] for i in range(256)]

width = cam.width
row = bytearray(width)

veml7700 = adafruit_veml7700.VEML7700(cam_i2c)
bh1750 = adafruit_bh1750.BH1750(cam_i2c)


# Set up I2C1 for display
print("Initializing display")
display_i2c = busio.I2C(board.GP27, board.GP26)
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
dy = 12

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

line4 = label.Label(
    terminalio.FONT, text=dummy_text, scale=1, color=0xFFFFFF, x=x_offset, y=y_offset+3*dy
)
splash.append(line4)

line5 = label.Label(
    terminalio.FONT, text=dummy_text, scale=1, color=0xFFFFFF, x=x_offset, y=y_offset+4*dy
)
splash.append(line5)


iso_ev = 0

while True:

    cam.capture(buf)

    for j in range(0, cam.height, 2):
        sys.stdout.write(f"\033[{j//2}H")
        for i in range(cam.width):
            row[i] = remap[buf[2 * (width * j + i)]]
        sys.stdout.write(row)
        sys.stdout.write("\033[K")
    sys.stdout.write("\033[J")

    #lux = veml7700.lux
    lux = bh1750.lux
    ev = math.log(lux * 0.4)

    aperture_ev = 0

    shutter_ev = ev + aperture_ev - iso_ev

    line1.text = f"iso: {100* 2**iso_ev}"
    line2.text = f"     f/{APERTURE_EV[aperture_ev]}"
    line3.text = f"ss:  {ev_to_shutter_speed(shutter_ev)}"

    line4.text = ""
    line5.text = f"ev:  {shutter_ev:.2f}"


    time.sleep(0.5)   

