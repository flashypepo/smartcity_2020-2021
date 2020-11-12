"""
demo openweather API-request

2020-1102 PP new - version 3 - functions
"""
import requests
from lib.secrets import OPENWEATHER_API_KEY

# configuration
OW_API_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weatherdata_from(city_name, country_code):
    """ get weather data for city_name and country_code,
        return weather data in JSON-format."""
    city = city_name
    # check for space in name, convert to url-encoded space
    if " " in city_name:
        city = city_name.replace(" ", "%20")
    url = f"{OW_API_URL}?q={city},{country_code}&APPID={OPENWEATHER_API_KEY}"
    # DEBUG: print(url)  # debug
    # get the weather data
    weather_data = requests.get(url)
    return weather_data.json()

def get_temp_max_celsius(data):
    """ return max.temperature in Celcius from data.
        data: JSON-format """
    # get max.temperature
    temp_max = data.get('main').get('temp_max')
    return (temp_max - 273.15)

def get_windspeed(data):
    """ return wind speed from data.
        data: JSON-format """
    return data.get('wind').get('speed')

def get_description(data):
    return data.get('weather')[0].get('description')


if __name__ == "__main__":
    city_name = "Almere Stad"
    weather_data = get_weatherdata_from(city_name, "NL")

    print(f"Weersrapport voor {city_name}")

    temp_max = get_temp_max_celsius(weather_data)
    wind_speed = get_windspeed(weather_data)
    description = get_description(weather_data)

    print("Beschrijving: {}".format(description))
    print ("Max.temperatuur: {:4.2f}\u00b0C".format(temp_max))
    print ("Wind snelheid: {:4.2f} m/s".format(wind_speed))
