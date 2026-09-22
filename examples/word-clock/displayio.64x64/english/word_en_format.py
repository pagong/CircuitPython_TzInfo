# SPDX-FileCopyrightText: 2023 Frederick M Meyer
#
# SPDX-License-Identifier: MIT
# Library for Word-Clock-EN

import random

###################

QUARTER = "Quarter"
HALF = "Half"
PAST = "Past"
UNTIL = "Until"
OCLOCK = "O'clock"
NOON = "Noon"
MIDNIGHT = "Midnight"
MINUTE = "Minute"
SINGLE_DIGITS = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
TEN_PLUS = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
TENS = ["Twenty", "Thirty", "Fourty", "Fifty"]

###################

def format_hour(hour_num):
    hour = hour_num % 24
    if hour == 0:
        o_hour = MIDNIGHT
    elif hour == 12:
        o_hour = NOON
    else:
        if hour > 12:
            hour -= 12
        elif hour == 0:
            hour = 12

        if hour < 10:
            o_hour = SINGLE_DIGITS[hour - 1]
        else:
            o_hour = TEN_PLUS[hour - 10]
    return hour, o_hour

COLOR_VALUES = [0, 128, 255]  # Brighter - Possible color values used for random 0..2 selection
#COLOR_VALUES = [0, 80, 160]   # Dimmer   - Possible color values used for random 0..2 selection
#COLOR_VALUES = [0, 64, 128]   # Dimmer   - Possible color values used for random 0..2 selection

def pick_random_color():
    # Pick a random color for each line and add it to the display
    r = COLOR_VALUES[random.randint(0, 2)]
    g = COLOR_VALUES[random.randint(0, 2)]
    b = COLOR_VALUES[random.randint(0, 2)]
    if not (r | g | b): r = g = b = COLOR_VALUES[2] # Set to white if black result
    return (r<<16|g<<8|b)

###################

def format_text(hour, minute):
    if minute <= 30:
        o_min_half = PAST
        hour, o_hour = format_hour(hour)
    else:
        o_min_half = UNTIL
        minute = 60 - minute
        hour, o_hour = format_hour(hour + 1)

    if minute == 15:
        o_min = QUARTER
    elif minute == 30:
        o_min = HALF
    elif minute == 0:
        o_min = ""
        o_min_half = ""
    elif minute < 10:
        o_min = SINGLE_DIGITS[minute - 1]
    elif minute < 20:
        o_min = TEN_PLUS[minute - 10]
    else:
        o_min = TENS[(minute // 10) - 2]
        if minute % 10:
            o_min += " " + SINGLE_DIGITS[(minute % 10) - 1]

    if o_min not in [QUARTER, HALF, ""]:
        o_min += " " + MINUTE
        if minute != 1: o_min += "s"

    if minute > 0 or o_hour in [MIDNIGHT, NOON]:
        txt = (o_min + " " + o_min_half + " " + o_hour).strip()
    else:
        txt = (o_min + " " + o_min_half + " " + o_hour + " " + OCLOCK).strip()

    return txt

###################
