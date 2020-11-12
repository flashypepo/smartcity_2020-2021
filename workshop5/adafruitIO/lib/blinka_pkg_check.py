"""
This Python script checks for the availability of 
Adafruit-Blinka Library Packages for the Raspberry Pi.

It does this by attempting to import the Python package 'board'.
If the package import is successful we report the package
as Available, and if the import (or import initialization)
fails for any reason, we report the package as Unavailable.

Built and tested with Python 3.7 on Raspberry Pi 4 Model B

2020-1017 PP new, based on: 
https://github.com/PacktPublishing/Practical-Python-Programming-for-IoT/blob/master/chapter01/gpio_pkg_check.py
"""
try:
    import board
    print('Adafruit-Blinka Available')
except:
    print('Adafruit-Blinka Unavailable. Install with "pip3 install Adafruit-Blinka"')
