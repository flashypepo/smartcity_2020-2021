"""
API weather example with Python library 'requests'

2020-0921 PP new, from Santos - project mini-weersvoorspeller
"""
import requests
from time import sleep
from lib.secrets import OPENWEATHER_API_KEY as APPID

CITY = "Bussum"
COUNTRY="NL"
METRIC = "metric"
WAIT = 300   # default 1 call in 5 minutes

def getWeatherDataFrom(city, country):
    q = "?q={0},{1}".format(city, country)
    # debug: print(q)
    url = "http://api.openweathermap.org/data/2.5/weather" + "{}".format(q) + "&appid={0}".format(APPID) + "&units={}".format(METRIC)
    # debug: print(url)
    data = requests.get(url)
    return data

def getTemp(data):
    return (data.json().get('main').get('temp'),data.json().get('main').get('temp_min'),data.json().get('main').get('temp_max'))

def getWindSpeed(data):
    return data.json().get('wind').get('speed')

def getHumidity(data):
    return data.json().get('main').get('humidity')

def getPressure(data):
    return data.json().get('main').get('pressure')

def getClouds(data):
    return data.json().get('clouds').get('all')

def getDescription(data):
    return data.json().get('weather')[0].get('description')

def main(wait=WAIT):
    # data limit to free service:
    # 50 calls per 60 seconds
    # -> minimum wait is 2 seconds
    if wait < 2:
        wait = 2  
    while True:
        weather_data = getWeatherDataFrom(CITY, COUNTRY)
        t, tmin, tmax = getTemp(weather_data)

        # print some weather data
        print("{0} - {1}".format(CITY, COUNTRY)) # top_line
        print("Desc: {}".format(getDescription(weather_data)))
        print("Temp: {0} ({1}-{2}) *C".format(t, tmin, tmax))
        print("Pres: {} hPa".format(getPressure(weather_data)))
        print("Humi: {} %".format(getHumidity(weather_data)))
        print("Wind: {} m/s".format(getWindSpeed(weather_data)))
        print("Clouds: {} %".format(getClouds(weather_data)))
        print("------------")
        sleep(wait)


if __name__ == "__main__":
    try:
        main(wait=5)  # wait is in seconds
    except KeyboardInterrupt:
        print('User interrupt... done')
