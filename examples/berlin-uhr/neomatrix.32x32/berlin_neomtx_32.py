# SPDX-FileCopyrightText: 2025-2026 Mike Doerr
# SPDX-License-Identifier: MIT
# Berlin clock (NeoMatrix: 32x32)

import neopixel
import neomatrix

from micropython import const

#######################################

# define color names
COL_RED     = 0xFF0000
COL_YELLOW  = 0xC0C000
COL_LIME    = 0x70C000
COL_ORANGE  = 0xC07000
COL_BLACK   = 0x000000
COL_GREY    = 0x171717
COL_BLUE    = 0x0000FF

# unused colors
COL_WHITE   = 0xFFFFFF
COL_GREEN   = 0x00FF00
COL_CYAN    = 0x00C0C0
COL_MAGENTA = 0xC000C0

#######################################

# Layout of rectangles of Berlin-Uhr
xoff = 1
yoff = 5

a = const(2)
b = const(2)
c = const(6)
d = const(4)
e = const(1)

# Four 6x4 rects for hour*5
x = xoff
y = yoff+2*b
hour5 = [ (x, y, c, d),
          (x+b+c, y, c, d),
          (x+2*b+2*c, y, c, d),
          (x+3*b+3*c, y, c, d) ]

# Four 6x4 rects for hour*1
x = xoff
y = yoff+3*b+d
hour1 = [ (x, y, c, d),
          (x+b+c, y, c, d),
          (x+2*b+2*c, y, c, d),
          (x+3*b+3*c, y, c, d) ]

# Eleven 2x4 rects for minutes*5
x = 0
y = yoff+3*b+2*d+b+e
minute5 = [ (x, y, a, d),
            (x+a+e, y, a, d),
            (x+2*a+2*e, y, a, d),
            (x+3*a+3*e, y, a, d),
            (x+4*a+4*e, y, a, d),
            (x+5*a+5*e, y, a, d),
            (x+6*a+6*e, y, a, d),
            (x+7*a+7*e, y, a, d),
            (x+8*a+8*e, y, a, d),
            (x+9*a+9*e, y, a, d),
            (x+10*a+10*e, y, a, d) ]

# Four 6x4 rects for minutes*1
x = xoff
y = yoff+4*b+3*d+b+e
minute1 = [ (x, y, c, d),
            (x+b+c, y, c, d),
            (x+2*b+2*c, y, c, d),
            (x+3*b+3*c, y, c, d) ]

#######################################

def Draw_hours(grid, hour):
    h5 = hour//5
    for i in range(4):
        rect = hour5[i]
        color = COL_RED if (i < h5) else COL_GREY
        grid.fill_rect(rect[0], rect[1], rect[2], rect[3], color)

    h1 = hour%5
    for i in range(4):
        rect = hour1[i]
        color = COL_ORANGE if (i < h1) else COL_GREY
        grid.fill_rect(rect[0], rect[1], rect[2], rect[3], color)


def Draw_minutes(grid, minute):
    m5 = minute//5
    for i in range(11):
        rect = minute5[i]
        color = COL_RED if (i%3) == 2 else COL_YELLOW
        if (i%3) == 1: color = COL_ORANGE
        if (i >= m5):  color = COL_GREY
        grid.rect(rect[0], rect[1], rect[2], rect[3], color)

    m1 = minute%5
    for i in range(4):
        rect = minute1[i]
        color = COL_YELLOW if (i < m1) else COL_GREY
        grid.fill_rect(rect[0], rect[1], rect[2], rect[3], color)


def Draw_seconds(grid, second):
    color = COL_LIME if (second & 1) else COL_GREY
    # blink the circle at the top
    x = 15 ; y = 1 ; l = 2
    grid.hline(x,   y,   l,   color)
    grid.hline(x-1, y+1, l+2, color)
    grid.hline(x-2, y+2, l+4, color)
    grid.hline(x-2, y+3, l+4, color)
    grid.hline(x-1, y+4, l+2, color)
    grid.hline(x,   y+5, l,   color)
    # show a bar in the middle
    barlen = 1 + second // 2
    y = yoff+3*b+2*d+e
    grid.hline(1, y, barlen, COL_BLUE)
    
#######################################

