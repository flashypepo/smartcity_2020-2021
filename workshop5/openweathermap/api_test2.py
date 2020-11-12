"""
demo openweather API-request

2020-1102 PP new - version 2 - variables
"""
import requests
from lib.secrets import OPENWEATHER_API_KEY

# configuration
OW_API_URL = "http://api.openweathermap.org/data/2.5/weather"

city_name = "Almere Stad".replace(" ", "%20")
print(city_name)
#city_name = "Bussum"
country_code = "NL"

url = f"{OW_API_URL}?q={city_name},{country_code}&APPID={OPENWEATHER_API_KEY}"
# DEBUG: print(url)  # debug

# get the weather data
weather_data = requests.get(url)

# get max.temperature
temp_max = weather_data.json().get('main').get('temp_max')
print(temp_max)   # temperatuur in Kelvin
print("{:4.2f}".format(temp_max - 273.15))  # temperatuur in Celcius
