"""
Weather forecast - demo webservice

op basis van code Project 7 in 
Santos, "Raspberry Pi Project Handboek"

Resources:
* i2c OLED display 128 * 64 pixels, SSD1306 chip
* Python 3
* Python libraries: requests, Adafruit blinka, adafruit_ssd1306
* Account en API-key op openweathermap.org
* Stad en Land voor de weersverwachtingen

OpenWeatherMap API:
https://openweathermap.org/appid/

2020-1103 PP versie 1 OLED-versie using class OpenWeatherMap

"""
# if class code is in subfolder 'lib': 
# add an empty file __init__.py
from lib.openweathermap import OpenWeaterMap

#import blinka_pkg_check
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# display a message of 3 lines, first line big font
def display_message(top_line, line_2):
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((0,0), top_line, font=largefont, fill=255)
    draw.text((0,50), line_2, font=smallfont, fill=255)
    disp.image(image)
    disp.show()


if __name__ == "__main__":
    city_name = "Bussum"  #"Almere Stad"
    country_code = "NL"
    print(f"Weersrapport voor {city_name} in {country_code}:")

    # prepare OLED-display ...
    # 1. setup display
    i2c = busio.I2C(board.SCL, board.SDA)
    disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c, reset=None) 
    # fonts can be found in '/usr/share/fonts/truetype/
    smallfont = ImageFont.truetype('FreeSans.ttf', 12)
    largefont = ImageFont.truetype('FreeSans.ttf', 33)
    # 2. clear display
    disp.fill(0)
    disp.show()
    # 3. make an image to draw on in 1-bit color
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)

    # get weather data for city...
    service = OpenWeaterMap(city_name, country_code)
    #service._test(city_name, country_code, wait=300)

    t, tmin, tmax = service.temperatures()
    # print some weather data
    topline = f"{city_name}"
    DEGREE = "\u00b0"  # unicode for degree-character
    line2 = "Temp: {0:2.1f} ({1:2.1f}-{2:2.1f}){3}C".format(t, tmin, tmax, DEGREE)
    print(f"{topline}\n{line2}")
    display_message(topline, line2)

    #print("JSON:\n{}".format(service._weatherdata_json()))
