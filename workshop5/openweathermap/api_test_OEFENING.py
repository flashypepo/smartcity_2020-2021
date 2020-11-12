"""
API weather example with Python library 'requests'

OEFENINGEN:
1. maak aan een eigen API-KEY en vul dat
   in onderstaande code voor APPID.
2. voeg toe wind snelheid (windspeed), zoals temperaturen
3. voeg toe luchtvochtigheid (humidity)
4. voeg toe luchtdruk (pressure)
5. wat lastiger: voeg toe beschrijving (description)
6. vul in voor city: "Almere Stad". Wat gaat er fout?

Potentiele resultaat is het volgende uitvoer in console:
Bussum - NL
Desc: clear sky
Temp: 11.61 (10.56-12.22) *C
Pres: 1019 hPa
Humi: 72 %
Wind: 3.13 m/s
Clouds: 0 %
------------

2020-1103 PP als oefening gemaakt
2020-0921 PP nieuw uit Santos - project mini-weersvoorspeller
"""
import requests
from time import sleep

# vergeet niet jouw API key in te vullen!
APPID = "xxxxxxxxxxxxxxxxxxx"
CITY = "Bussum"
COUNTRY="NL"
METRIC = "metric"

def getWeatherDataFrom(city, country):
    q = "?q={0},{1}".format(city, country)
    # debug: print(q)
    url = "http://api.openweathermap.org/data/2.5/weather" + "{}".format(q) + "&appid={0}".format(APPID) + "&units={}".format(METRIC)
    # debug: print(url)
    data = requests.get(url)
    return data

def getTemp(data):
    temp = data.json().get('main').get('temp')
    temp_min = data.json().get('main').get('temp_min')
    temp_max = data.json().get('main').get('temp_max')
    return (temp, temp_min, temp_max)

def getClouds(data):
    return data.json().get('clouds').get('all')


if __name__ == "__main__":
    try:
        weather_data = getWeatherDataFrom(CITY, COUNTRY)
        t, tmin, tmax = getTemp(weather_data)

        # print some weather data
        print("{0} - {1}".format(CITY, COUNTRY)) # top_line
        #print("Desc: {}".format(getDescription(weather_data)))
        print("Temp: {0} ({1}-{2}) *C".format(t, tmin, tmax))
        #print("Pres: {} hPa".format(getPressure(weather_data)))
        #print("Humi: {} %".format(getHumidity(weather_data)))
        #print("Wind: {} m/s".format(getWindSpeed(weather_data)))
        print("Clouds: {} %".format(getClouds(weather_data)))
        print("------------")
    except KeyboardInterrupt:
        print('User interrupt... done')
