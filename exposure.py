# SPDX-FileCopyrightText: 2025 Aaron Marburg
#
# SPDX-License-Identifier: Unlicense
"""
Author: Aaron Marburg (aaron.marburg@gmail.com)


"""

import math

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


def calculate_shutter_ev( lux, aperture_ev, iso_ev):

    if lux > 0:
        ev = math.log(lux * 0.4)
    else:
        ev = 0

    aperture_ev = 0

    return ev + aperture_ev - iso_ev
