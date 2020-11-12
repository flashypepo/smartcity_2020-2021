"""
demo openweather API-request

OpenWeatherMap API:
https://openweathermap.org/appid/

Pricing and limits Free account:
https://openweathermap.org/price

Kelvin to Celsius: 
https://www.rapidtables.com/convert/temperature/kelvin-to-celsius.html

2020-1102 PP new - version 1
Gebaseerd op [Santos] Raspberry Pi Project Handboek
"""
import requests
from lib.secrets import OPENWEATHER_API_KEY

weather_data = requests.get(
    "http://api.openweathermap.org/data/2.5/weather?q=Bussum,NL&APPID={}".format(OPENWEATHER_API_KEY)
)

# get maximum temperature
temp_max = weather_data.json().get('main').get('temp_max')
print(temp_max) 
# explanation API: https://openweathermap.org/current#current_JSON









""" extra code ------------------
temp_max is in Kelvin
temp_max_c = temp_max - 273.15
print("{:4.2f}".format(temp_max_c))  # temperatuur in Celcius
"""
