####
#
#   This is an ugly MVP/POC of running both light systems of the same controller
#
#######3
import time         # Both
import board        # Both
import asyncio      # Threading

import neopixel     # PSI/HOLO

import digitalio                        # FLD/RLD
from adafruit_max7219 import matrices   # FLD/RLD
import busio                            # FLD/RLD
import random                           # FLD/RLD


# Init color definitions
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
COLORS = [ RED,YELLOW,GREEN,CYAN,BLUE,PURPLE ]


# NeoPixel light basic config
pixel_pin = board.GP14                      # Pin for connecting to the first neopixel lights
NEOPIXEL_BRIGHTNESS = 0.4                   # Overall brightness
LIGHT_PIXELS = [ 8, 8, 8, 8, 8 ]            # The led count for each sequential light
LIGHT_BRIGHTNESS = [ 1, 1, 1, 0.1, 0.1 ]    # relitive brightness of each light
TOTAL_PIXELS = sum(LIGHT_PIXELS)            # Total Pixel Count
MORPH_STEPS = 20
MORPH_DELAY = 0.1

# MAX7291 Basic Config
DIS_WIDTH = 48
DIS_HEIGHT = 8
SCROLL_TIMES = 8
SCROLL_LENGTH = DIS_WIDTH * SCROLL_TIMES
MATRIX_BRIGHTNESS = 3 # INT 0 -> 15
MATRIX_PINS = [ board.GP2, board.GP3, board.GP1 ]   # clock, MOSI, CS



# NeoPixel automation Config
LIGHT_INIT_COLORS = [ GREEN,BLUE,BLUE,GREEN,GREEN ]
LIGHT_AUTOMATIONS = { }
LIGHT_AUTOMATIONS["FRONT_PSI"] = { "light" : 0, "colors" : [ BLUE,YELLOW ] }
LIGHT_AUTOMATIONS["BACK_PSI"] = { "light" : 1, "colors" : [ RED,YELLOW,GREEN ] }


# Init automation counters
for automation in LIGHT_AUTOMATIONS:
    LIGHT_AUTOMATIONS[automation]["current"] = 0




# Init NeoPixel lib
dome = neopixel.NeoPixel(pixel_pin, TOTAL_PIXELS, brightness=NEOPIXEL_BRIGHTNESS, auto_write=False)

# Init max7291 lib

spi = busio.SPI(clock=MATRIX_PINS[0], MOSI=MATRIX_PINS[1])
cs = digitalio.DigitalInOut(MATRIX_PINS[2])

matrix = matrices.CustomMatrix(spi, cs, DIS_WIDTH, DIS_HEIGHT)




def set_light_color(light_number,color):

    pixels = LIGHTS[light_number]
    brightness = LIGHT_BRIGHTNESS[light_number]

    COLOR = tuple(brightness * v for v in color)
    for pixel in pixels:
        dome[pixel] = COLOR

    dome.show()


async def morph_light(light_number,end_color,steps,delay):

    #print("Starting morph: " + str(light_number))

    pixels = LIGHTS[light_number]
    start_color = dome[pixels[0]]
    brightness = LIGHT_BRIGHTNESS[light_number]

    for i in range(steps + 1):
        interpolated = tuple(
            int(start_color[j] + (end_color[j] - start_color[j]) * i / steps)
            for j in range(len(start_color))
        )

        COLOR = tuple(brightness * v for v in interpolated)

        for pixel in pixels:
            dome[pixel] = COLOR
        dome.show()
        await asyncio.sleep(delay)

    #print("morph done for: " + str(light_number))


async def scroll_matrix():

    VALUES = [ ]

    for row in range(DIS_WIDTH):
        col_vals  = [ ]
        for column in range(DIS_HEIGHT):
            v = random.randrange(0,2)
            col_vals.append(v)
        VALUES.append(col_vals)


    SCROLL_COUNTER = 0
    while SCROLL_COUNTER < SCROLL_LENGTH:

        #print(SCROLL_COUNTER)

        await asyncio.sleep(0.1)

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





async def main():

    matrix_task = asyncio.create_task(scroll_matrix())

    tasks = [ ]

    for automation in LIGHT_AUTOMATIONS:
        light = LIGHT_AUTOMATIONS[automation]["light"]
        step = LIGHT_AUTOMATIONS[automation]["current"]
        color = LIGHT_AUTOMATIONS[automation]["colors"][step]

        if step == len(LIGHT_AUTOMATIONS[automation]["colors"]) -1:
            LIGHT_AUTOMATIONS[automation]["current"] = 0
        else:
            LIGHT_AUTOMATIONS[automation]["current"] += 1

        task = asyncio.create_task(morph_light(light,color,MORPH_STEPS,MORPH_DELAY))
        tasks.append(task)




    #await asyncio.gather(task,matrix_task)
    await asyncio.gather(task) # ,matrix_task)
    matrix_task.cancel()








# Initialise lights as off
dome.fill((0,0,0))
dome.show()
matrix.fill(False)
matrix.show()
matrix.brightness(MATRIX_BRIGHTNESS)



# create list of neopixel lights
LIGHTS = [ ]
c = 0
for light in LIGHT_PIXELS:
    pxls = list(range(c,c + light))
    c += light
    LIGHTS.append(pxls)


# Set initial colors of neopixels
for l in range(0,len(LIGHTS)):
    init_color = LIGHT_INIT_COLORS[l]
    set_light_color(l,init_color)



while True:
    asyncio.run(main())







