# SPDX-FileCopyrightText: 2023 Frederick M Meyer
# German version: 2026 Mike Doerr
# SPDX-License-Identifier: MIT
# Library for Word-Clock-DE 

import random

###################

QUARTER = "Viertel"
QUARTER3 = "Drei Viertel"
HALF = "Halb"
PAST = "nach"
UNTIL = "vor"
OCLOCK = "Uhr"
SDIGITS = ["Null", "Ein", "Zwei", "Drei", "Vier", "Fuenf", "Sechs", "Sieben", "Acht", "Neun"]
TEN_PLUS = ["Zehn", "Elf", "Zwoelf", "Dreizehn", "Vierzehn", "Fuenfzehn", "Sechzehn", "Siebzehn", "Achtzehn", "Neunzehn"]
TENS = ["zwanzig", "dreissig", "vierzig", "fuenfzig"]
DAYPHASE = ["Nachts", "Morgens", "Mittags", "Abends"]
PHASES = [ [22,23,0,1,2,3,4], [5,6,7,8,9,10], [11,12,13,14,15,16], [17,18,19,20,21] ]
ONE = "Eins"
AND = "und"
BLANK = " "

###################

def format_hour(hour_num):
    hour = hour_num % 24
    if hour > 12:
        hour -= 12
    if hour < 10:
        o_hour = SDIGITS[hour]
    else:
        o_hour = TEN_PLUS[hour - 10]
    return hour, o_hour

def day_phase(hour_num):
    hour = hour_num % 24
    if hour in PHASES[0]:
        o_phase = DAYPHASE[0]
    elif hour in PHASES[1]:
        o_phase = DAYPHASE[1]
    elif hour in PHASES[2]:
        o_phase = DAYPHASE[2]
    elif hour in PHASES[3]:
        o_phase = DAYPHASE[3]
    return o_phase

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

def format_minute(minute):
    o_min = ""

    if minute == 1:
        o_min = ONE
    elif minute == 15:
        o_min = QUARTER
    elif minute == 30:
        o_min = HALF
    elif minute == 45:
        o_min = QUARTER3
    elif minute < 10:
        o_min = SDIGITS[minute]
    elif minute < 20:
        o_min = TEN_PLUS[minute - 10]
    else:
        if minute % 10:
            o_min = SDIGITS[(minute % 10)] + AND + BLANK
        o_min += TENS[(minute // 10) - 2]

    o_min_half = PAST
    if (minute % 30) >= 20:
        o_min_half = UNTIL
    return o_min_half, o_min

###################

def format_text(hour, minute):
    o_min_half, o_min = format_minute(minute)

    if (o_min_half == UNTIL):
        dummy, o_min = format_minute(30 - (minute % 30))

    if o_min in [QUARTER, HALF, QUARTER3]:
        o_min_half = UNTIL
    else:
        if (o_min_half == UNTIL):
            o_min += BLANK + UNTIL
            if minute < 30:
                o_min += BLANK + HALF

    if (o_min_half == UNTIL):
        o_phase = day_phase(hour + 1)
        hour, o_hour = format_hour(hour + 1)
    else:
        o_phase = day_phase(hour)
        hour, o_hour = format_hour(hour)

    txt = "Es ist "
    if minute == 0:
        txt += (o_hour + BLANK + OCLOCK + BLANK + o_phase)
    elif (o_min_half == PAST):
        txt += (o_hour + BLANK + OCLOCK + BLANK + o_min)
    else:
        if hour == 1:
            o_hour = ONE
        elif hour == 0:
            hour, o_hour = format_hour(12)
        txt += (o_min + BLANK + o_hour)

    return txt

###################

