# SK 6812 rgbw led strip controller for raspberry pi

## Disclaimer:
English is not my native language, but I do my best. Constructive remarks are welcome and 
appreciated.  

This program is originally made for my personal use only. If you want to use it or
take inspire from it, do as you wish. If you need help on anything you may ask me a
question, without any guarantee of response (I will try to respond anyway).

## Prerequisites:
You must have tkinter installed. On Linux simply run `sudo apt-get install python3-tk`  
You also have to install python packages `guizero` and `rpi_ws281x`  
Before using, you must set the number of leds you are using in `Colors.py`

## How to use:
*This section is not finished*  
Simply run `Colors.py` (or `GUI.py` for a nice user interface).
When running `Colors.py`, enter the color you want when `c` is displayed 
(colors are of the form `r, g, b, w` where r, g, b and w are values between 0 and 255)
and the alpha value when `a` is displayed.
