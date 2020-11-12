"""
'dht_adafruitio.py'
==================================
Example of sending temperature and humidity
sensor values to an Adafruit IO feed.

Sensor: DHT11 connected to GPIO10

Dependencies:
1. adafruit blinka
    'pip3 install adafruit-blinka'
2. adafruit DHT library
    'pip3 install adafruit-circuitpython-dht'
3. package 'libgpiod2'
    'sudo apt-get install libgpiod2'
4. Adafruit IO Python Client
    'pip3 install adafruit-io'
    (https://github.com/adafruit/io-client-python)

2020-1110 PP new Adafruit IO feeds
2020-1104 PP new, DHT11 sensor
Based upon Python code from Brent Rubell
Tutorial Link: Tutorial Link: https://learn.adafruit.com/adafruit-io-basics-temperature-and-humidity
"""
# import standard python modules.
import time

# import adafruit board and dht library (blinka).
import board
import adafruit_dht

# import Adafruit IO REST client.
from Adafruit_IO import Client, Feed

# Set to your Adafruit IO username and Adafruit IO key
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
from lib.secrets import ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY

# Delay in-between sensor readings, in seconds.
DHT_READ_TIMEOUT = 900 # 15 minuten

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Set up Adafruit IO Feeds.
# dashboard: DHT sensordata
temperature_feed = aio.feeds('dht-temperature')
humidity_feed = aio.feeds('dht-humidity')

# setup environment sensor
# Set up DHT11 Sensor at GPIO10
env_sensor = adafruit_dht.DHT11(board.D10)
 
while True:
    try:
        # get sensor values
        temperature = env_sensor.temperature
        humidity = env_sensor.humidity

        if humidity is not None \
            and temperature is not None:
            print('Temp={0:0.1f}\u00b0C Humidity={1:0.1f}%'.format(temperature, humidity))

            # Send humidity and temperature feeds to Adafruit IO
            temperature = '{:4.2f}'.format(temperature)
            humidity = '{:4.2f}'.format(humidity)
            aio.send(temperature_feed.key, str(temperature))
            aio.send(humidity_feed.key, str(humidity))

    except RuntimeError as error:
        # Errors happen fairly often, 
        # DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        env_sensor.exit()
        raise error

    # Timeout to avoid flooding Adafruit IO
    print(f"waiting {DHT_READ_TIMEOUT} seconds...")
    time.sleep(DHT_READ_TIMEOUT)
