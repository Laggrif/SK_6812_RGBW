import time

from rpi_ws281x import *

import Strandtest
import sys

# LED strip configuration:

LED_COUNT      = 150      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0
#LED_STRIP      = ws.SK6812_STRIP_RGBW
LED_STRIP      = ws.SK6812W_STRIP


def ShowDouble(strip, color):
    #for i in range(84):
    #    strip.setPixelColor(68 + i, Decoder(f.read()))
    m = 1
    for i in range(42):
        strip.setPixelColor(68+i, color)
        strip.setPixelColor(strip.numPixels()- i - 1, color)
        strip.show()
        time.sleep(1.6/(m))
        m = m+2

def Show(strip, color):
    for i in range(84):
        strip.setPixelColor(68 + i, color)
    strip.show()
    
def rainbow(strip, thread):
    while True:
        if thread.stopped():
            break
        for j in range(256):
            for i in range(strip.numPixels() - 68):
                if thread.stopped():
                    break
                strip.setPixelColor(i+68, Strandtest.wheel((i+j) & 255))
            strip.show()
            time.sleep(20/1000.0)
            if thread.stopped():
                break

def Decoder(str):
    colors = []
    c = ""
    string = str
    for i in range(len(string)):
        if string[0] != ",":
            c += string[0]
        elif string[0] == ",":
            colors.append(int(c))
            c = ""
        string = string[1:]
    colors.append(int(c))
    if (len(colors) != 4):
        print("error")
        print(len(colors))
        return
    return colors

def ColorFromList(colors):
    return Color(colors[1], colors[0], colors[2], colors[3])

def InitStrip(alpha):
    LED_BRIGHTNESS = alpha
    try:
        strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL,
                                  LED_STRIP)
    except:
        print("aie")
    strip.begin()
    strip.setBrightness(alpha)
    return strip

def Write(colors, alpha):
    f = open("/Shared/previousColor.txt", "w")
    f.write(colors + '\n')
    f.write(alpha)
    f.close()


if __name__ == '__main__':
    #strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    #strip.begin()
    if len(sys.argv) > 1:

        if len(sys.argv) == 3:
            alpha = sys.argv[2]
        else:
            alpha = "255"

        arg1 = sys.argv[1]
        programs = ["rb", "th"]

        try:
            arg1 = int(sys.argv[1])
        except:
            pass

        if arg1 in programs:
            strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, int(alpha), LED_CHANNEL, LED_STRIP)
            strip.begin()
            if arg1 == programs[0]:
                while True:
                    Strandtest.rainbow(strip)
            if arg1 == programs[1]:
                while True:
                    Strandtest.theaterChaseRainbow(strip)
        else:
            if arg1 == "d":
                arg1 = "0,0,0,0"
                """
                strip = InitStrip(int(alpha))
                Show(strip, ColorFromList(Decoder(arg1)))
                Write(arg1, alpha)
                sys.exit(arg1 + "," + alpha)
                """
            elif arg1 == "r":
                arg1 = "255,0,0,0"
            elif arg1 == "g":
                arg1 = "0,255,0,0"
            elif arg1 == "b":
                arg1 = "0,0,255,0"
            elif arg1 == "w":
                arg1 = "0,0,40,255"

            else:
                sys.exit(f"Bad input, input was \"{sys.argv[1]}\"")

            f = open("/Shared/previousColor.txt", "r")
            content = f.readlines()
            oldColors = Decoder(content[0])
            oldAlpha = int(content[1])
            f.close()

            strip = InitStrip(int(alpha))

            oldAlpha2 = oldAlpha/int(alpha)
            if oldAlpha < int(alpha):
                for i in range(len(oldColors)):
                    if int(oldColors[i] * oldAlpha2) >= 1 :
                        oldColors[i] = int(oldColors[i] * oldAlpha2)
                    else:
                        oldColors[i] = 0
            print(oldColors)
            oldColors = ColorFromList(oldColors)
            colors = Decoder(arg1)

            if len(sys.argv) != 3:
                Show(strip, oldColors)

                ShowDouble(strip, ColorFromList(colors))
            else:
                Show(strip, ColorFromList(colors))
            Write(arg1, alpha)

        print(arg1 + "," + alpha)

    else:
        r=0
        g=0
        b=0
        w=0

        while True:
            i = input("c")
            if i == "exit":
                sys.exit("Successfully Shut down")
            a = input("a")
            if a == "exit":
                sys.exit("Successfully Shut down")
            try:
                #r = input("r")
                #Show(strip, Color(g, r, b ,w))
                #g = int(input("g"))
                #Show(strip, Color(g, r, b ,w))
                #b = int(input("b"))
                #Show(strip, Color(g, r, b ,w))
                #w = int(input("w"))
                #Show(strip, Color(g, r, b ,w))
                strip = InitStrip(int(a))
                strip.setBrightness(100)
                Show(strip, ColorFromList(Decoder(i)))
            except:
                print(f"bad input :")
