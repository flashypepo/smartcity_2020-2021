"""
class OpenWeatherMap
get weather data from the OpenWeaterMap service

Dependencies:
Python library requests
secrets.py contains API-KEY

OpenWeatherMap API:
https://openweathermap.org/appid/

Pricing and limits Free account:
https://openweathermap.org/price

Kelvin to Celsius: 
https://www.rapidtables.com/convert/temperature/kelvin-to-celsius.html

Source based upon [Santos] Raspberry Pi Project Handboek

2020-1102 PP new, refactored source code to OOP-class
"""
from time import sleep
import requests
try:
    from lib.secrets import OPENWEATHER_API_KEY
except ImportError:
    from secrets import OPENWEATHER_API_KEY

# URL of OpenWeatherMaps API
OW_API_URL = "http://api.openweathermap.org/data/2.5/weather"

class OpenWeaterMap():
    def __init__(self, city_name, country_code, unit="metric"):
        """ get weather data for city_name and country_code,
            store weather data in JSON-format."""
        self._api_url = OW_API_URL
        self._apiid = OPENWEATHER_API_KEY
        # get the weather data
        self._data_json = self.getWeatherDataFrom(city_name, country_code, unit)

    # supposed to be a private method
    def _getURLCityName(self, city_name):
        # check for space in name, convert to url-encoded space
        url_city = city_name
        if " " in city_name:
            url_city = city_name.replace(" ", "%20")
        return url_city

    # core method: get weather data from city
    def getWeatherDataFrom(self, city_name, country_code="NL", unit="metric"):
        """ 
        getWeatherDataFrom() - get weather data from OpenWeatherMap
            city_name: name of the city
            country_code: code of the country, default: "NL"
            unit: units of the values, default: "metric"
        returns: weather data in JSON-format
        """
        # check city_name is url-valid
        url_city = self._getURLCityName(city_name)
        q = "?q={0},{1}".format(url_city, country_code)
        # debug: print(q)
        #url = "http://api.openweathermap.org/data/2.5/weather" + "{}".format(q) + "&appid={0}".format(APPID) + "&units={}".format(METRIC)
        url = OW_API_URL \
        + "{}".format(q) \
        + "&appid={}".format(self._apiid) \
        + "&units={}".format(unit)
        # debug: print(url)
        data = requests.get(url)
        return data.json()

    # =============
    # services
    # =============
    def temperatures(self):
        data = self._data_json  # get data
        temp    = data.get('main').get('temp')
        minTemp = data.get('main').get('temp_min')
        maxTemp = data.get('main').get('temp_max')
        return (temp, minTemp, maxTemp)

    def windspeed(self):
        return self._data_json.get('wind').get('speed')

    def description(self):
        return self._data_json.get('weather')[0].get('description')

    def humidity(self):
        return self._data_json.get('main').get('humidity')

    def pressure(self):
        return self._data_json.get('main').get('pressure')

    def clouds(self):
        return self._data_json.get('clouds').get('all')

    # add yourself more methods which returns a specifc weather data

    # kind of private method, returns weather_data in JSON
    def _weatherdata_json(self):
        return self._data_json

    # test method - quick test if class code works
    # add yourself more specific weather data
    # wait between weatherdata calls: 5 minutes
    # due to data limit of the service
    def _test(self, city="Bussum", country="NL", wait=300):
        DEGREE = "\u00b0"  # unicode for degree-character
        service = OpenWeaterMap(city, country)
        while True:
            t, tmin, tmax = service.temperatures()

            # print some weather data
            print("{0} - {1}".format(city, country)) # top_line
            print("Desc: {}".format(service.description()))
            print("Temp: {0} {1}C".format(t, DEGREE))
            # print("Temp: {0} ({1}-{2}) {3}C".format(t, tmin, tmax, DEGREE))
            print("Pres: {} hPa".format(service.pressure()))
            print("Humi: {} %".format(service.humidity()))
            print("Wind: {} m/s".format(service.windspeed()))
            print("Clouds: {} %".format(service.clouds()))
            print("------------")
            sleep(wait)

# test method
if __name__ == "__main__":
    city_name = "Almere Stad"
    country_code = "NL"
    print(f"Weersrapport voor {city_name} in {country_code}:")
    service = OpenWeaterMap(city_name, country_code)
    #service._test(city_name, country_code, wait=300)
    t, tmin, tmax = service.temperatures()
    # print some weather data
    DEGREE = "\u00b0"  # unicode for degree-character
    print("Temp: {0} ({1}-{2}){3}C".format(t, tmin, tmax, DEGREE))
    print("JSON:\n{}".format(service._weatherdata_json()))
