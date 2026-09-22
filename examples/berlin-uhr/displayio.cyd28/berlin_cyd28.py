# SPDX-FileCopyrightText: 2026 Mike Doerr
# SPDX-License-Identifier: MIT
# Berlin-Uhr (for LCD ILI9341, with TZinfo)

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

import fourwire
import adafruit_ili9341

from berlin_display_32 import Init_All, Draw_hours, Draw_minutes, Draw_seconds
import tzinfo
import gc

###################

# define some global constants
from micropython import const
Scale = const(6)
H = const(320)
W = const(240)
L = const(32)

BRIGHTNESS = 0.1
SLEEP = 0.1

###################

# Release any resources currently in use for the displays
displayio.release_displays()

# pin defs for CYD (Cheap Yellow Display = Sunton 2432S032)
spi = board.LCD_SPI()
tft_cs = board.LCD_CS
tft_dc = board.LCD_DC
tft_bl = board.LCD_BCKL

display_bus = fourwire.FourWire(spi, command=tft_dc, chip_select=tft_cs)
DISPLAY = adafruit_ili9341.ILI9341(display_bus, width=W, height=H, backlight_pin=tft_bl, bgr=True)

###################

# Wifi details are in settings.toml file
WLAN_SSID = os.getenv('CIRCUITPY_WIFI_SSID')
WLAN_PASS = os.getenv('CIRCUITPY_WIFI_PASSWORD')

print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])
print("Connecting to %s"%WLAN_SSID)

try:
    wifi.radio.connect(WLAN_SSID, WLAN_PASS)
    pool = socketpool.SocketPool(wifi.radio)

    print("Connected to %s!"%WLAN_SSID)
    print("My IP address: ", wifi.radio.ipv4_address)

    ntp = adafruit_ntp.NTP(pool, server="de.pool.ntp.org", tz_offset=0)
    dtm = ntp.datetime
except:
    dtm = time.struct_time( (2026, 3, 14,   22, 44, 0,    5, 0, 0) )

###################

POSIX_TZ = os.getenv('POSIX_TZ')
if not POSIX_TZ:
    # Default is Central Europe
    POSIX_TZ = "CET-1CEST,M3.5.0,M10.5.0/3"
# initialize TZinfo cache
our_tz = tzinfo.TZInfo(POSIX_TZ)
print(POSIX_TZ)

print(dtm)
rtc.RTC().datetime = dtm

################### Create hierarchy of layers

# import functions from berlin_display and initialize ROOT group
DISPLAY.root_group = Init_All(Scale)

DISPLAY.root_group.scale = Scale
DISPLAY.root_group.y = (H - L * Scale) // 2
DISPLAY.root_group.x = (W - L * Scale) // 2

################### Main LOOP: query RTC and use displayio to draw the berlin clock

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

