# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
Author: Mark Roberts (mdroberts1243) from Adafruit code
This test will initialize the display using displayio and draw a solid white
background, a smaller black rectangle, miscellaneous stuff and some white text.

"""


import board
import displayio
import time
import sdcardio
import storage

# Sensors connected via Stemma
import adafruit_bh1750
import supervisor
import busio
import digitalio
from adafruit_mcp230xx.mcp23008 import MCP23008

import adafruit_ov5640

from camera import Camera
from tft import TftDisplay
from oled import OledDisplay
from sdcard import SdCard
from exposure import calculate_shutter_ev

displayio.release_displays()
# oled_reset = board.D9

dir(board)
print(f"Run reason: {supervisor.runtime.run_reason}")

# Use the board's primary SPI bus
spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)

# Initialize SD card first
sdcard = SdCard(spi)

tft = TftDisplay(spi, adafruit_ov5640.OV5640_SIZE_QVGA)

#== Connect to camera

print("construct camera")
sensor_i2c = board.STEMMA_I2C()
cam = Camera(sensor_i2c, bitmap=tft.bitmap)

bh1750 = adafruit_bh1750.BH1750(sensor_i2c)

# Configure MCP23008
i2c1 = busio.I2C(board.GP27, board.GP26)
mcp = MCP23008(i2c1)

# 3 is backlight
p = mcp.get_pin(3)
p.direction = digitalio.Direction.OUTPUT
p.value = False
time.sleep(0.5)
p.value = True

# All on OLED
# 4 == SW3
# 5 == SW4
# 6 == SW2
# 7 == SW5 (Reset pin)

for pin_num in [4,5,6,7]:
    p = mcp.get_pin(pin_num)
    p.direction = digitalio.Direction.INPUT
    p.pull = digitalio.Pull.UP


iso_ev = 0
aperture_ev = 0

while True:
    buf = cam.capture()

    # for j in range(0, cam.height, 2):
    #     sys.stdout.write(f"\033[{j//2}H")
    #     for i in range(cam.width):
    #         row[i] = remap[buf[2 * (width * j + i)]]
    #     sys.stdout.write(row)
    #     sys.stdout.write("\033[K")
    # sys.stdout.write("\033[J")

    lux = bh1750.lux

    shutter_ev = calculate_shutter_ev(lux, aperture_ev, iso_ev)
    
    
    tft.bitmap.dirty()
    tft.refresh(minimum_frames_per_second=0)

    # line1.text = f"iso: {100* 2**iso_ev}"
    # line2.text = f"     f/{APERTURE_EV[aperture_ev]}"
    # line3.text = f"ss:  {ev_to_shutter_speed(shutter_ev)}"

    # line4.text = ""
    # line5.text = f"ev:  {shutter_ev:.2f}"

    # for pin_num in [4,5,6,7]:
    #     p = mcp.get_pin(pin_num)
    #     print(f"Pin {pin_num}: {p.value}")

    time.sleep(0.5)   

