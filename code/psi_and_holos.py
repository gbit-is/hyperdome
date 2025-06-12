# Write your code here :-)
import time
import board
from rainbowio import colorwheel
import neopixel
import asyncio

# Init color definitions
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
COLORS = [ RED,YELLOW,GREEN,CYAN,BLUE,PURPLE ]


pixel_pin = board.GP0                       # Pin for connecting to the first neopixel lights
BRIGHTNESS = 0.4                            # Overall brightness
LIGHT_PIXELS = [ 8, 8, 8, 8, 8 ]            # The led count for each sequential light
LIGHT_BRIGHTNESS = [ 1, 1, 1, 0.1, 0.1 ]    # relitive brightness of each light
TOTAL_PIXELS = sum(LIGHT_PIXELS)            # Total Pixel Count
MORPH_STEPS = 20
MORPH_DELAY = 0.1


LIGHT_INIT_COLORS = [ GREEN,BLUE,BLUE,GREEN,GREEN ]

LIGHT_AUTOMATIONS = { }

LIGHT_AUTOMATIONS["FRONT_PSI"] = { "light" : 0, "colors" : [ BLUE,YELLOW ] }
LIGHT_AUTOMATIONS["BACK_PSI"] = { "light" : 1, "colors" : [ RED,YELLOW,GREEN ] }


for automation in LIGHT_AUTOMATIONS:
    LIGHT_AUTOMATIONS[automation]["current"] = 0




# Init NeoPixel lib
dome = neopixel.NeoPixel(pixel_pin, TOTAL_PIXELS, brightness=BRIGHTNESS, auto_write=False)

dome.fill((0,0,0))
dome.show()

LIGHTS = [ ]

c = 0
for light in LIGHT_PIXELS:
    pxls = list(range(c,c + light))
    c += light

    LIGHTS.append(pxls)



def set_light_color(light_number,color):

    pixels = LIGHTS[light_number]
    brightness = LIGHT_BRIGHTNESS[light_number]

    COLOR = tuple(brightness * v for v in color)
    for pixel in pixels:
        dome[pixel] = COLOR

    dome.show()


async def morph_light(light_number,end_color,steps,delay):

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




for l in range(0,len(LIGHTS)):
    init_color = LIGHT_INIT_COLORS[l]
    set_light_color(l,init_color)




async def main():

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




    await asyncio.gather(task)





while True:
    asyncio.run(main())







