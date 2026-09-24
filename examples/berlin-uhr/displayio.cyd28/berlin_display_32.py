# SPDX-FileCopyrightText: 2026 Mike Doerr
# SPDX-License-Identifier: MIT
# Berlin clock (DisplayIO: 32x32)

import displayio

from micropython import const

############### Define color palettes for pixel_shaders

# define color names
COL_RED     = 0xFF0000
COL_YELLOW  = 0xC0C000
COL_LIME    = 0x70C000
COL_ORANGE  = 0xC07000
COL_BLACK   = 0x000000
COL_GREY    = 0x202020
COL_BLUE    = 0x0000FF

# unused colors
COL_WHITE   = 0xFFFFFF
COL_GREEN   = 0x00FF00
COL_CYAN    = 0x00C0C0
COL_MAGENTA = 0xC000C0

############### 

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
Hour5 = [ (x, y, c, d),
          (x+b+c, y, c, d),
          (x+2*b+2*c, y, c, d),
          (x+3*b+3*c, y, c, d) ]

# Four 6x4 rects for hour*1
x = xoff
y = yoff+3*b+d
Hour1 = [ (x, y, c, d),
          (x+b+c, y, c, d),
          (x+2*b+2*c, y, c, d),
          (x+3*b+3*c, y, c, d) ]

# Eleven 2x4 rects for minutes*5
x = 0
y = yoff+3*b+2*d+b+e
Minute5 = [ (x, y, a, d),
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
Minute1 = [ (x, y, c, d),
            (x+b+c, y, c, d),
            (x+2*b+2*c, y, c, d),
            (x+3*b+3*c, y, c, d) ]

############### Create Bitmaps

# A "RECT" is a 6x4 Bitmap with 2 colors: 0 = transparent outer part, 1 = filled interior
BM_RECT = displayio.Bitmap(6, 4, 2)

y = 0
BM_RECT[0, y] = 1 ; BM_RECT[1, y] = 1 ; BM_RECT[2, y] = 1 ; BM_RECT[3, y] = 1 ; BM_RECT[4, y] = 1 ; BM_RECT[5, y] = 1
y = 1
BM_RECT[0, y] = 1 ; BM_RECT[1, y] = 1 ; BM_RECT[2, y] = 1 ; BM_RECT[3, y] = 1 ; BM_RECT[4, y] = 1 ; BM_RECT[5, y] = 1
y = 2
BM_RECT[0, y] = 1 ; BM_RECT[1, y] = 1 ; BM_RECT[2, y] = 1 ; BM_RECT[3, y] = 1 ; BM_RECT[4, y] = 1 ; BM_RECT[5, y] = 1
y = 3
BM_RECT[0, y] = 1 ; BM_RECT[1, y] = 1 ; BM_RECT[2, y] = 1 ; BM_RECT[3, y] = 1 ; BM_RECT[4, y] = 1 ; BM_RECT[5, y] = 1


# A "SMALL" is a 2x4 Bitmap with 2 colors: 0 = transparent outer part, 1 = filled interior
BM_SMALL = displayio.Bitmap(2, 4, 2)

y = 0 ; BM_SMALL[0, y] = 1 ; BM_SMALL[1, y] = 1 
y = 1 ; BM_SMALL[0, y] = 1 ; BM_SMALL[1, y] = 1 
y = 2 ; BM_SMALL[0, y] = 1 ; BM_SMALL[1, y] = 1 
y = 3 ; BM_SMALL[0, y] = 1 ; BM_SMALL[1, y] = 1 


# A "CIRC" is a 6x6 Bitmap with 2 colors: 0 = transparent outer part, 1 = filled interior
BM_CIRC = displayio.Bitmap(6, 6, 2)

y = 0
BM_CIRC[0, y] = 0 ; BM_CIRC[1, y] = 0 ; BM_CIRC[2, y] = 1 ; BM_CIRC[3, y] = 1 ; BM_CIRC[4, y] = 0 ; BM_CIRC[5, y] = 0
y = 1
BM_CIRC[0, y] = 0 ; BM_CIRC[1, y] = 1 ; BM_CIRC[2, y] = 1 ; BM_CIRC[3, y] = 1 ; BM_CIRC[4, y] = 1 ; BM_CIRC[5, y] = 0
y = 2
BM_CIRC[0, y] = 1 ; BM_CIRC[1, y] = 1 ; BM_CIRC[2, y] = 1 ; BM_CIRC[3, y] = 1 ; BM_CIRC[4, y] = 1 ; BM_CIRC[5, y] = 1
y = 3
BM_CIRC[0, y] = 1 ; BM_CIRC[1, y] = 1 ; BM_CIRC[2, y] = 1 ; BM_CIRC[3, y] = 1 ; BM_CIRC[4, y] = 1 ; BM_CIRC[5, y] = 1
y = 4
BM_CIRC[0, y] = 0 ; BM_CIRC[1, y] = 1 ; BM_CIRC[2, y] = 1 ; BM_CIRC[3, y] = 1 ; BM_CIRC[4, y] = 1 ; BM_CIRC[5, y] = 0
y = 5
BM_CIRC[0, y] = 0 ; BM_CIRC[1, y] = 0 ; BM_CIRC[2, y] = 1 ; BM_CIRC[3, y] = 1 ; BM_CIRC[4, y] = 0 ; BM_CIRC[5, y] = 0


# A "BAR" is a 30x1 Bitmap with 2 colors: 0 = BLACK, 1 = BLUE
BM_BAR = displayio.Bitmap(30, 1, 2)

############### Create Palettes

# Create 2 element palette for storing colors
color_values = 2

PAL_BAR = displayio.Palette(color_values)
PAL_BAR[0] = COL_BLACK
PAL_BAR[1] = COL_BLUE

PAL_GREY = displayio.Palette(color_values)
PAL_GREY[0] = 0
PAL_GREY[1] = COL_GREY
PAL_GREY.make_transparent(0)

PAL_YELLOW = displayio.Palette(color_values)
PAL_YELLOW[0] = 0
PAL_YELLOW[1] = COL_YELLOW

PAL_ORANGE = displayio.Palette(color_values)
PAL_ORANGE[0] = 0
PAL_ORANGE[1] = COL_ORANGE

PAL_RED = displayio.Palette(color_values)
PAL_RED[0] = 0
PAL_RED[1] = COL_RED

PAL_LIME = displayio.Palette(color_values)
PAL_LIME[0] = 0
PAL_LIME[1] = COL_LIME
PAL_LIME.make_transparent(0)

############### Create TileGrids 

color_values = 2

GRP_HOUR5 = displayio.Group()
def init_hour5():
    for num in range(len(Hour5)):
        # use a separate palette for each rect
        pal = displayio.Palette(color_values)
        # make a tilegrid for each rect
        tg = displayio.TileGrid(bitmap=BM_RECT, pixel_shader=pal)
        pos = Hour5[num]
        tg.x = pos[0]
        tg.y = pos[1]
        GRP_HOUR5.append(tg)

GRP_HOUR1 = displayio.Group()
def init_hour1():
    for num in range(len(Hour1)):
        # use a separate palette for each rect
        pal = displayio.Palette(color_values)
        # make a tilegrid for each rect
        tg = displayio.TileGrid(bitmap=BM_RECT, pixel_shader=pal)
        pos = Hour1[num]
        tg.x = pos[0]
        tg.y = pos[1]
        GRP_HOUR1.append(tg)

GRP_MIN5 = displayio.Group()
def init_min5():
    for num in range(len(Minute5)):
        # use a separate palette for each rect
        pal = displayio.Palette(color_values)
        # make a tilegrid for each rect
        tg = displayio.TileGrid(bitmap=BM_SMALL, pixel_shader=pal)
        pos = Minute5[num]
        tg.x = pos[0]
        tg.y = pos[1]
        GRP_MIN5.append(tg)

GRP_MIN1 = displayio.Group()
def init_min1():
    for num in range(len(Minute1)):
        # use a separate palette for each rect
        pal = displayio.Palette(color_values)
        # make a tilegrid for each rect
        tg = displayio.TileGrid(bitmap=BM_RECT, pixel_shader=pal)
        pos = Minute1[num]
        tg.x = pos[0]
        tg.y = pos[1]
        GRP_MIN1.append(tg)

GRP_SEC1 = displayio.Group()
def init_sec1():
    # use a separate palette for circ
    pal = displayio.Palette(color_values)
    # make a tilegrid for circ
    tg = displayio.TileGrid(bitmap=BM_CIRC, pixel_shader=pal)
    tg.x = 13
    tg.y = 1
    GRP_SEC1.append(tg)

GRP_BAR1 = displayio.Group()
def init_bar1():
    # use a separate palette for circ
    pal = displayio.Palette(color_values)
    # make a tilegrid for circ
    tg = displayio.TileGrid(bitmap=BM_BAR, pixel_shader=pal)
    tg.x = 1
    tg.y = yoff+3*b+2*d+e
    GRP_BAR1.append(tg)
    
############### 

def Init_All(scale=1):
    init_hour5()
    init_hour1()
    init_min5()
    init_min1()
    init_sec1()
    init_bar1()

    # create DisplayIo group hierarchy
    ROOT = displayio.Group()

    ROOT.append(GRP_HOUR5)
    ROOT.append(GRP_HOUR1)
    ROOT.append(GRP_MIN5)
    ROOT.append(GRP_MIN1)
    ROOT.append(GRP_SEC1)
    ROOT.append(GRP_BAR1)

    return ROOT

############### Define some drawing functions

def Draw_hours(hour):
    h5 = hour//5
    for i in range(4):
        rect = GRP_HOUR5[i]
        palette = PAL_RED if (i < h5) else PAL_GREY
        rect.pixel_shader = palette

    h1 = hour%5
    for i in range(4):
        rect = GRP_HOUR1[i]
        palette = PAL_ORANGE if (i < h1) else PAL_GREY
        rect.pixel_shader = palette

############### 

def Draw_minutes(minute):
    m5 = minute//5
    for i in range(11):
        rect = GRP_MIN5[i]
        palette = PAL_RED if (i%3) == 2 else PAL_YELLOW
        if (i%3) == 1: palette = PAL_ORANGE
        if (i >= m5):  palette = PAL_GREY
        rect.pixel_shader = palette

    m1 = minute%5
    for i in range(4):
        rect = GRP_MIN1[i]
        palette = PAL_YELLOW if (i < m1) else PAL_GREY
        rect.pixel_shader = palette

############### 

def Draw_seconds(second):
    # blink the circle at the top
    palette = PAL_LIME if (second & 1) else PAL_GREY
    circ = GRP_SEC1[0]
    circ.pixel_shader = palette

    # show a bar in the middle
    bar = GRP_BAR1[0]
    palette = PAL_BAR
    bar.pixel_shader = palette
    barlen = 1 + second // 2
    for x in range(30):
        if x < barlen:
            bar.bitmap[x, 0] = 1  # COL_BLUE
        else:
            bar.bitmap[x, 0] = 0  # COL_BLACK

############### 

