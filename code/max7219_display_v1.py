import time
import board
import digitalio
from adafruit_max7219 import matrices
import busio
import random

DIS_WIDTH = 48
DIS_HEIGHT = 8
SCROLL_TIMES = 8
SCROLL_LENGTH = DIS_WIDTH * SCROLL_TIMES
BRIGHTNESS = 3 # INT 0 -> 15


# You may need to change the chip select pin depending on your wiring
spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP4)
cs = digitalio.DigitalInOut(board.GP1)

matrix = matrices.CustomMatrix(spi, cs, DIS_WIDTH, DIS_HEIGHT)

# VCC -> 5V
# GND -> GND
# DIN -> GP3
# CS  -> GP1
# CLK -> GP2


matrix.fill(False)
matrix.show()

matrix.brightness(BRIGHTNESS)

while True:

    VALUES = [ ]

    for row in range(DIS_WIDTH):
        col_vals  = [ ]
        for column in range(DIS_HEIGHT):
            v = random.randrange(0,2)
            col_vals.append(v)
        VALUES.append(col_vals)


    SCROLL_COUNTER = 0
    while SCROLL_COUNTER < SCROLL_LENGTH:

        ROW = 0
        for column in VALUES:
            COLUMN = 0
            for led in column:
                matrix.pixel(ROW,COLUMN,led)
                COLUMN += 1
            ROW += 1

        VALUES = VALUES[-1:] + VALUES[:-1]
        matrix.show()

        SCROLL_COUNTER += 1
