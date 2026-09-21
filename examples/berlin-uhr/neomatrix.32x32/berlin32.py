# SPDX-FileCopyrightText: 2025-2026 Mike Doerr
# SPDX-License-Identifier: MIT
# Berlin clock (NeoMatrix: 32x32)

import time
import board
import os
import rtc

import wifi
import socketpool
import ssl
import adafruit_ntp
import adafruit_requests

import neopixel
import neomatrix

from matrix32 import MatrixSetup
from berlin_neomtx_32 import Draw_hours, Draw_minutes, Draw_seconds

import tzinfo

#######################################

NUM_COLS = 32
NUM_CELLS = 32
NUM_PIXEL = (NUM_COLS * NUM_CELLS)

BRIGHTNESS = 0.1
SLEEP = 0.1

# NEO_PIN is for WaveShare ESP32-S3-Zero
NEO_PIN = board.IO1

# NEO_PIN is for Pico-W
#NEO_PIN = board.GP28

# create the matrix of tiles
matrix = MatrixSetup(NEO_PIN, "vstripes", BRIGHTNESS)

#######################################

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

#######################################

POSIX_TZ = os.getenv('POSIX_TZ')
if not POSIX_TZ:
    # Default is Central Europe
    POSIX_TZ = "CET-1CEST,M3.5.0,M10.5.0/3"
# initialize TZinfo cache
our_tz = tzinfo.TZInfo(POSIX_TZ)
print(POSIX_TZ)

print(dtm)
rtc.RTC().datetime = dtm

#######################################

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
        # clear the matrix
        matrix.fill(0)

        Draw_minutes(matrix, minute)
        Draw_hours(matrix, hour)

    if second != last_sec:
        last_sec = second
        # blink second mark
        Draw_seconds(matrix, second)

        # show the matrix
        matrix.display()

    time.sleep(SLEEP)

