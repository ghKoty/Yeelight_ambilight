import os
import win32gui
import time
import yeelight
from win32api import GetSystemMetrics

# start get config
config = [line.strip() for line in open("config.txt", 'r')] #load config file
fps = ""
ip = ""
pixelPos = ""
pixelX = ""
pixelY = ""
canTurnOff = ""
offThreshold = ""
changeEffect = ""
changeEffectDuration = ""
debug = ""
optimization = ""
# end get config

# start read config
fps = int(config[1])
ip = config[3]
pixelPos = config[5]
pixelX = config[7]
pixelY = config[9]
canTurnOff = bool(config[11])
offThreshold = int(config[13])
changeEffect = config[15]
changeEffectDuration = int(config[17])
debug = bool(config[19])
optimization = bool(config[21])
# end read config

if ip == "a":
    ip = input("Bulb IP: ")
bulb = yeelight.Bulb(ip, effect=changeEffect, duration=changeEffectDuration) # connect to lamp
bulb.start_music() # start music mode, to get unlimited packages
bulb.turn_on()
bulb.set_color_temp(4000)
bulb.set_brightness(100)

# start pixel position set
if pixelX == "a": # set pixel X position automatically
    if pixelPos == "bl" or pixelPos == "tl" or pixelPos == "l":
        pixelX = 2
    elif pixelPos == "br" or pixelPos == "tr" or pixelPos == "r":
        pixelX = int(GetSystemMetrics(0)-2)
    else:
        pixelX = int(GetSystemMetrics(0)/2)
    if debug:
        print("pixelX set automatically: ", pixelX)
else: # set pixel X position manualy
    pixelX = int(pixelX)
    if debug:
        print("pixelX set manualy: ", pixelX)
if pixelY == "a": # set pixel Y position automatically
    if pixelPos == "tl" or pixelPos == "tr" or pixelPos == "t":
        pixelY = 2
    elif pixelPos == "br" or pixelPos == "bl" or pixelPos == "b":
        pixelY = int(GetSystemMetrics(1)-2)
    else:
        pixelY = int(GetSystemMetrics(1)/2)
    if debug:
        print("pixelY set automatically: ", pixelY)
else: # set pixel X position manualy
    pixelY = int(pixelY)
    if debug:
        print("pixelY set manualy: ", pixelY)
# end pixel position set

r = 0
g = 0
b = 0
oldR = 0
oldG = 0
oldB = 0

def get_pixel_colour(i_x, i_y): # get color of current pixel on screen
    global r, g, b
    i_desktop_window_id = win32gui.GetDesktopWindow()
    i_desktop_window_dc = win32gui.GetWindowDC(i_desktop_window_id)
    long_colour = win32gui.GetPixel(i_desktop_window_dc, i_x, i_y)
    i_colour = int(long_colour)
    win32gui.ReleaseDC(i_desktop_window_id,i_desktop_window_dc)
    r = (i_colour & 0xff)
    g = ((i_colour >> 8) & 0xff)
    b = ((i_colour >> 16) & 0xff)

def maximum(a, b, c):
    if (a >= b) and (a >= c):
        largest = a
    elif (b >= a) and (b >= c):
        largest = b
    else:
        largest = c
    return largest

print("OK")

while True: # main loop
    get_pixel_colour(pixelX, pixelY)
    if debug:
        print("Input data: r=" + str(r) + ", g=" + str(g) + ", b=" + str(b))
    if oldR != r or oldG != g or oldB != b or not optimization: # check is color changed if optimization=0
        if maximum(r, g, b) <= offThreshold: # check is brightness of pixel less than off threshold
            if not canTurnOff:
                print("seted to 1 1 1 1")
                bulb.set_rgb(1, 1, 1)
                bulb.set_brightness(1)
            else:
                bulb.set_rgb(r, g, b)
                bulb.set_brightness(int((((((maximum(r, g, b) - 0) * (100 - 0)) / (255 - 0)) + 0))))
                bulb.turn_off()
        else:
            if canTurnOff:
                bulb.turn_on()
            bulb.set_rgb(r, g, b)
            if debug:
                print("brightness: " + str(int((((((maximum(r, g, b) - 0) * (100 - 0)) / (255 - 0)) + 0)))))
            bulb.set_brightness(int((((((maximum(r, g, b) - 0) * (100 - 0)) / (255 - 0)) + 0))))
    oldR = r
    oldG = g
    oldB = b
    time.sleep(1/fps)
