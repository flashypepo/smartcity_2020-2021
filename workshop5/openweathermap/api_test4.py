"""
demo openweather API-request

2020-1102 PP new - version 4 - class OpenWeatherMap
"""
import requests
from lib.secrets import OPENWEATHER_API_KEY

class OpenWeaterMap():
    def __init__(self, city_name, country_code):
        """ get weather data for city_name and country_code,
            store weather data in JSON-format."""
        self._api_url = "http://api.openweathermap.org/data/2.5/weather"
        self._api_key = OPENWEATHER_API_KEY
        city = city_name
        # check for space in name, convert to url-encoded space
        if " " in city_name:
            city = city_name.replace(" ", "%20")
        url = f"{self._api_url}?q={city},{country_code}&APPID={self._api_key}"
        # DEBUG: print(url)  # debug
        # get the weather data
        data = requests.get(url)
        self._weather_data_json = data.json()

    def max_temp_celsius(self):
        """ return max. temperature in Celcius 
            from weather data """
        # get max.temperature
        temp_max = self._weather_data_json.get('main').get('temp_max')
        return (temp_max - 273.15)

    def windspeed(self):
        return self._weather_data_json.get('wind').get('speed')

    def description(self):
        return self._weather_data_json.get('weather')[0].get('description')
    
    # more methods which returns a specifc weather data


if __name__ == "__main__":
    city_name = "Almere Stad"
    service = OpenWeaterMap(city_name, "NL")

    print(f"Weersrapport voor {city_name}")

    # haal op de weersgegeven voor city_name
    temp_max = service.max_temp_celsius()
    wind_speed = service.windspeed()
    description = service.description()

    # toon de weersgegevesn in console
    print("Beschrijving: {}".format(description))
    print ("Max.temperatuur: {:4.2f}\u00b0C".format(temp_max))
    print ("Wind snelheid: {:4.2f} m/s".format(wind_speed))
