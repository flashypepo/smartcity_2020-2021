"""
'bme680_adafruitio.py'
==================================
Example of sending temperature and humidity
sensor values to an Adafruit IO feed.

Sensor: BME680 connected to i2c, address=0x76

Dependencies:
1. adafruit blinka
    'pip3 install adafruit-blinka'
2. adafruit BME680 library
    'pip3 install adafruit-circuitpython-bme680'
    Note BME280 library:
        'pip3 install adafruit-circuitpython-bme280'
3. package 'libgpiod2'
    'sudo apt-get install libgpiod2'
4. Adafruit IO Python Client
    'pip3 install adafruit-io'
    (https://github.com/adafruit/io-client-python)

2020-1104 PP new, BME680 sensor
Based upon Python code from Brent Rubell
Tutorial Link: Tutorial Link: https://learn.adafruit.com/adafruit-io-basics-temperature-and-humidity
"""
# import standard python modules.
import time

# import adafruit board library (blinka).
import board
# import adafruit i2c library (blinka).
from busio import I2C
# import adafruit bme680 library (blinka).
import adafruit_bme680

# import Adafruit IO REST client.
from Adafruit_IO import Client, Feed

# Set to your Adafruit IO username and Adafruit IO key
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
from lib.secrets import ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY

# Delay in-between sensor readings, in seconds.
# data limit Adafruit IO: 30 data points per minute
# or in 'n' secs upload maximum 'n/2' datapoints
SENSOR_READ_TIMEOUT = 10  # in seconds, max 5 datapoints

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Set up Adafruit IO Feeds.
temperature_feed = aio.feeds('temperature')
humidity_feed = aio.feeds('humidity')
pressure_feed = aio.feeds('pressure')
#TODO: altitude_feed = aio.feeds('altitude')
gas_feed = aio.feeds('gas')

# setup environment sensor
# Set up BME680 Sensor at I2C
i2c = I2C(board.SCL, board.SDA)
BME680_I2CADDRESS = 0x77  # BME280: 0x76
env_sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c, BME680_I2CADDRESS)
 
def calibrate(value):
    print(f"... BME680 sensor calibrating for sea level pressure: {value}")
    env_sensor.sea_level_pressure = value
    assert env_sensor.sea_level_pressure == value

""" 
location's pressure (hPa) at sea level from:
https://www.weatheronline.co.uk/weather/maps/current?LANG=en&CONT=euro&REGION=0003&LAND=NL&LEVEL=4&R=310&CEL=C&ART=tabelle&TYP=druck
The value changes the Alt-value!
I use 'Amsterdam/Schiphol' sea level value
"""
calibrate(1025)  # 10 Nov 2020 19:00

while True:
    try:
        # get sensor values
        temperature = env_sensor.temperature
        humidity = env_sensor.humidity
        pressure = env_sensor.pressure
        altitude = env_sensor.altitude
        gas = env_sensor.gas

        if humidity is not None \
            and temperature is not None:
            print('Temperature={0:0.1f}\u00b0C\tHumidity={1:0.1f}%\tPressure={2:0.1f}hPa'.format(temperature, humidity, pressure))
            print('Altitude   ={0:0.1f} m\tGas={1:} Ohm'.format(altitude, gas))
            #print('Gas={:} Ohm'.format(gas))

            # Send humidity and temperature feeds to Adafruit IO
            temperature = '{:0.1f}'.format(temperature)
            humidity = '{:0.1f}'.format(humidity)
            pressure = '{:0.1f}'.format(pressure)
            altitude = '{:0.1f}'.format(altitude)
            gas = '{:}'.format(gas)
            # data limit free account:
            # 30 data points per minute
            # -> make selection of data send to Adafruit IO
            aio.send(temperature_feed.key, str(temperature))
            aio.send(humidity_feed.key, str(humidity))
            aio.send(pressure_feed.key, str(pressure))
            # TODO: aio.send(altitude_feed.key, str(altitude))
            aio.send(gas_feed.key, str(gas))

    except RuntimeError as error:
        # Errors happen fairly often, 
        # DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        raise error

    # Timeout to avoid flooding Adafruit IO
    time.sleep(SENSOR_READ_TIMEOUT)
