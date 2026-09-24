# SPDX-FileCopyrightText: 2026 Mike Doerr
# SPDX-License-Identifier: MIT
# Berlin-Uhr: 64x64 HUB75 RGB Matrix

# Select "Adafruit" or "SeenGreat" for RGB Matrix Adapter
# - Code for Adafruit Matrix Portal S3
# - Code for SeenGreat RGB Matrix Adapter for ESP32-S3-DevKitC-1-N16 (without PSRAM !!)

import random
import os
import time
import rtc
import board
import busio

import ssl
import wifi
import socketpool
import adafruit_ntp
import adafruit_requests

import displayio
import framebufferio
import rgbmatrix

from berlin_display_32 import Init_All, Draw_hours, Draw_minutes, Draw_seconds
import tzinfo
import gc

##############

# define some global constants
from micropython import const
Scale = const(2)
H = const(64)
W = const(64)
L = const(32)

BRIGHTNESS = 0.1
SLEEP = 0.1

##############

# Release any resources currently in use for the displays
displayio.release_displays()

RGB_TYPE = "SeenGreat"
#RGB_TYPE = "Adafruit"

def seengreat_rgb():
    # Code for ESP32-S3-DevKitC-1 on SeenGreat RGB Matrix Adapter Board
    return rgbmatrix.RGBMatrix(
        width=W, height=H, bit_depth=3,
        rgb_pins=[
            board.IO37,   # R1
            board.IO6,    # G1
            board.IO36,   # B1
            board.IO35,   # R2
            board.IO5,    # G2
            board.IO0,    # B2
        ],
        addr_pins=[
            board.IO45,  # Addr-A
            board.IO1,   # Addr-B
            board.IO48,  # Addr-C
            board.IO2,   # Addr-D
            board.IO4,   # Addr-E
        ],
        clock_pin=board.IO47,
        latch_pin=board.IO38,
        output_enable_pin=board.IO21
    )

def adafruit_rgb():
    # Code for ESP32-S3 on Adafruit Matrix Portal S3
    return rgbmatrix.RGBMatrix(
        width=W, height=H, bit_depth=3,
        rgb_pins=[
            board.MTX_R1,
            board.MTX_G1,
            board.MTX_B1,
            board.MTX_R2,
            board.MTX_G2,
            board.MTX_B2
        ],
        addr_pins=[
            board.MTX_ADDRA,
            board.MTX_ADDRB,
            board.MTX_ADDRC,
            board.MTX_ADDRD,
            board.MTX_ADDRE
        ],
        clock_pin=board.MTX_CLK,
        latch_pin=board.MTX_LAT,
        output_enable_pin=board.MTX_OE
    )

if RGB_TYPE == "SeenGreat":
    MATRIX = seengreat_rgb()
elif RGB_TYPE == "Adafruit":
    MATRIX = adafruit_rgb()
else:
    raise NameError(RGB_TYPE)

DISPLAY = framebufferio.FramebufferDisplay(MATRIX, auto_refresh=False)

##############

# Wifi details are in settings.toml file
WLAN_SSID = os.getenv('CIRCUITPY_WIFI_SSID')
WLAN_PASS = os.getenv('CIRCUITPY_WIFI_PASSWORD')

print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])
print("Connecting to %s"%WLAN_SSID)

try:
#if True:
    wifi.radio.connect(WLAN_SSID, WLAN_PASS)
    pool = socketpool.SocketPool(wifi.radio)

    print("Connected to %s!"%WLAN_SSID)
    print("My IP address: ", wifi.radio.ipv4_address)

    ntp = adafruit_ntp.NTP(pool, server="de.pool.ntp.org", tz_offset=0)
    dtm = ntp.datetime
except:
    dtm = time.struct_time( (2026, 9, 15,    21, 0, 0,    0, 0, 0) )

##############

POSIX_TZ = os.getenv('POSIX_TZ')
if not POSIX_TZ:
    # Default is Central Europe
    POSIX_TZ = "CET-1CEST,M3.5.0,M10.5.0/3"
# initialize TZinfo cache
our_tz = tzinfo.TZInfo(POSIX_TZ)
print(POSIX_TZ)

print(dtm)
rtc.RTC().datetime = dtm

############## Create hierarchy of layers

# import functions from berlin_display and initialize ROOT group
DISPLAY.root_group = Init_All(Scale)

DISPLAY.root_group.scale = Scale
DISPLAY.root_group.y = (H - L * Scale) // 2
DISPLAY.root_group.x = (W - L * Scale) // 2

############## Main LOOP: query RTC and use displayio to draw the berlin clock

last_sec = -1
last_min = -1
last_utc = -1

# Main loop
while True:
    utc = time.time()
    if utc != last_utc:
        last_utc = utc
        lt = our_tz.utc_to_local(utc)
        hour   = lt.tm_hour
        minute = lt.tm_min
        second = lt.tm_sec

    # update berlin clock once per minute
    if minute != last_min:
        last_min = minute

        Draw_hours(hour)
        Draw_minutes(minute)
        print(gc.mem_free())

    if second != last_sec:
        last_sec = second
        # blink second mark
        Draw_seconds(second)

        # show the matrix
        DISPLAY.refresh()

    time.sleep(SLEEP)

