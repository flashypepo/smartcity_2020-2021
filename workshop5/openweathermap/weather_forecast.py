"""
Weather forecast - demo webservice

op basis van code Project 7 in 
Santos, "Raspberry Pi Project Handboek"

Layout:
    City
    Decription
    Temperature
    Pressure
    Humidity
    Wind
Note: maak je eigen layout met de weersgegevens

Resources:
* i2c OLED display 128 * 64 pixels, SSD1306 chip
* Python 3
* Python libraries: requests, Adafruit blinka, adafruit_ssd1306
* Account en API-key op openweathermap.org
* Stad en Land voor de weersverwachtingen

OpenWeatherMap API:
https://openweathermap.org/appid/

2020-1103 PP OLED-versie using class OpenWeatherMap
             final version: 6 lines on OLED, 
                            added partial timed loop
"""
import time

# if class code is in subfolder 'lib': 
# add an empty file __init__.py
from lib.openweathermap import OpenWeaterMap

#import blinka_pkg_check
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

WAIT = 30  # seconds between weaterdata requests
# data limit: max 50 calls per 60 seconds
#             minimum: 1 request per 2 seconds
#             for testing: value 5 is okay

def clear_image(refresh=False):
    # clear image
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    if refresh is True:
        disp.image(image)
        disp.show()

# display a message of 6 lines
# line_4, line_5, line_6 could be empty
def display_message(top_line, line_2, line_3, line_4="", line_5="", line_6=""):
    clear_image()
    # variabls for drawing area
    padding = 2
    top = padding
    x = padding
    # draw all lines
    # topline in bold font
    draw.text((x,top), top_line, font=boldfont, fill=255)
    draw.text((x,top+11), line_2, font=smallfont, fill=255)
    draw.text((x,top+21), line_3, font=smallfont, fill=255)
    draw.text((x,top+31), line_4, font=smallfont, fill=255)
    draw.text((x,top+41), line_5, font=smallfont, fill=255)
    draw.text((x,top+51), line_6, font=smallfont, fill=255)
    # display result
    disp.image(image)
    disp.show()

# alternative: draw line which contains '\n',
# and is considered a multiline text
def display_multiline(line):
    clear_image()
    # variabls for drawing area
    padding = 2
    top = padding
    x = padding
    # draw all lines
    draw.text((x,top), line, \
        font=smallfont2, fill=255, \
        spacing=1, align="left")
    # display result
    disp.image(image)
    disp.show()

# main execution ...
def run(city_name, country_code):
    # get weather data for city...
    service = OpenWeaterMap(city_name, country_code)
    # DEBUG: service._test(city_name, country_code, wait=300)
    # get relevant weather data
    t, _, _ = service.temperatures()
    descr = service.description()
    pressure = service.pressure()
    humidity = service.humidity()
    windspeed = service.windspeed()
    # show weather data
    DEGREE = "\u00b0"  # unicode for degree-character
    topline = f"{city_name} - {country_code}"
    line2 = "Desc   {}".format(descr)
    line3 = "Temp   {0:2.1f} {1}C".format(t, DEGREE)
    line4 = "Pres   {0:2.1f} hPa".format(pressure)
    line5 = "Hum    {} %".format(humidity)
    line6 = "Wind   {:2.1f} m/s".format(windspeed)
    # on console ...
    print(f"{topline}\n{line2}\n{line3}\n{line4}\n{line5}\n{line6}")
    # on OLED-display ...
    display_message(topline, line2, line3, line4, line5, line6)
    # alternative display function:
    # display_multiline(f"{topline}\n{line2}\n{line3}\n{line4}\n{line5}\n{line6}")

# # TODO: show progress either in console either on OLED
def mysleep(wait):
    start_time = time.time()
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > seconds:
            print("---------------")
            break


if __name__ == "__main__":
    city_name = "Bussum"  #"Almere Stad"
    country_code = "NL"
    print(f"Weersrapport voor {city_name} in {country_code}:")
    try:
        # prepare OLED-display ...
        # 1. setup display
        i2c = busio.I2C(board.SCL, board.SDA)
        disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c, reset=None) 
        # fonts can be found in '/usr/share/fonts/truetype/
        smallfont = ImageFont.truetype('FreeSans.ttf', 12)
        smallfont2 = ImageFont.truetype('FreeSans.ttf', 10)
        boldfont = ImageFont.truetype('FreeSansBold.ttf', 12)
        largefont = ImageFont.truetype('FreeSans.ttf', 33)
        # 2. clear display
        disp.fill(0)
        disp.show()
        # 3. make an image to draw on in 1-bit color
        width = disp.width
        height = disp.height
        image = Image.new('1', (width, height))
        draw = ImageDraw.Draw(image)

        while True:
            # get weather data for city...
            run(city_name, country_code)
            # check minimum: 1 request in 2 seconds
            seconds = WAIT if WAIT > 2 else 2
            print(f"{seconds} seconden wachten...")
            mysleep(seconds)
            # time.sleep(seconds)

    except KeyboardInterrupt:
        clear_image(True)
        print("Demo done!")
