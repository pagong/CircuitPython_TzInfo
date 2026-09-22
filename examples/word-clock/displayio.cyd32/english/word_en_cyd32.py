# SPDX-FileCopyrightText: 2023 Frederick M Meyer
# Optimized version: 2026 Mike Doerr
# SPDX-License-Identifier: MIT
# Word-Clock-EN (for LCD ST7789, with TZinfo)

import random
import os
import time
import rtc
import board
import busio

import digitalio
import terminalio
import adafruit_display_text as adt
import adafruit_display_text.label as adtl

import ssl
import wifi
import socketpool
import adafruit_ntp
import adafruit_requests

import displayio
import framebufferio
import fourwire
import adafruit_st7789

from word_en_format import format_text, pick_random_color
import tzinfo
import gc

###################

# define some global constants
from micropython import const
Scale = const(3)
H = const(320)
W = const(240)
L = const(64)

###################

# Release any resources currently in use for the displays
displayio.release_displays()

# pin defs for CYD (Cheap Yellow Display = Sunton 2432S032)
spi = board.LCD_SPI()
tft_cs = board.LCD_CS
tft_dc = board.LCD_DC
tft_bl = board.LCD_BCKL

display_bus = fourwire.FourWire(spi, command=tft_dc, chip_select=tft_cs)
DISPLAY = adafruit_st7789.ST7789(display_bus, width=W, height=H, backlight_pin=tft_bl)

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

###################

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

    if last_min != minute:
        last_min = minute

        text = format_text(hour, minute)
        text_list = adt.wrap_text_to_pixels(text, 60, font=terminalio.FONT)
        
        total_height = 0
        max_width = 0
        line_list = []
        for w in text_list:
            line = adtl.Label(terminalio.FONT,
                              color=pick_random_color(),
                              text=w, scale=1)
            line_list.append(line)
            zx, zy, zwidth, zheight = line.bounding_box
            total_height += zheight
            max_width = max(max_width, zwidth)

        xwork = ((60 - max_width) // 2) + 2
        ywork = ((60 - total_height) // 2) + 2 + 6

        current_y = ywork        
        g = displayio.Group(scale=Scale)
        for l in line_list:
            l.x = xwork
            l.y = current_y
            zx, zy, zwidth, zheight = l.bounding_box
            current_y += zheight
            g.append(l)

        DISPLAY.root_group=g
        print(gc.mem_free())

    time.sleep(1)

