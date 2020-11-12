"""  TODO  TODO  TODO
`bm680_mqttclient.py`
---------------------------------------------------------
Example of reading and writing to a shared  Adafruit IO Feed.
learn.adafruit.com/adafruit-io-basics-feeds/sharing-a-feed
Author: Brent Rubell for Adafruit Industries 2018

2020-1105 PP adopted for an environment sensor (BME680)
"""
# Import standard python modules.
import sys
import time
import random

# import adafruit board library (blinka).
import board
# import adafruit i2c library (blinka).
from busio import I2C
# import adafruit bme680 library (blinka).
import adafruit_bme680

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
from lib.secrets import ADAFRUIT_IO_KEY, ADAFRUIT_IO_USERNAME

# keep in mind the data limit!
SENSOR_READ_TIMEOUT = 10  # 1800  # 1x30 minuten, in seconds

# Shared IO Feed
# Make sure you have read AND write access to this feed to publish.
IO_FEED = 'MQTT-demofeed'  # feed to publish
TEMPERATURE_FEED = 'dht-temperature'  # feed to listen

# setup environment sensor
# this case: BME680 Sensor at I2C
# i2c = I2C(board.SCL, board.SDA)
# BME680_I2CADDRESS = 0x77
# env_sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c, BME680_I2CADDRESS)


# Define callback functions which will be called when certain events happen.
def connected(client):
    """Connected function will be called 
       when the client connects.
    """
    client.subscribe(IO_FEED)


def disconnected(client):
    """Disconnected function will be called
       when the client disconnects.
    """
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

temp_value = 0
def message(client, feed_id, payload):
    """Message function will be called when a subscribed feed 
       has a new value.
       The feed_id parameter identifies the feed, 
       and the payload parameter has the new value.
    """
    print(f"Feed '{feed_id}' received new value: {payload}")
    # publish it to MQTT dashboard
    client.publish(IO_FEED, payload)


# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect       =   connected
client.on_disconnect    =   disconnected
client.on_message       =   message

# Connect to the Adafruit IO server.
client.connect()
client.loop_background()
print(f'Publishing a new message when DHT11 feed received a new temperature...')

# print(f'Publishing a new message every {SENSOR_READ_TIMEOUT} seconds (press Ctrl-C to quit)...')
# while True:
#     try:
#         # temperature = env_sensor.temperature
#         # humidity = env_sensor.humidity
#         # pressure = env_sensor.pressure
#         # altitude = env_sensor.altitude
#         # gas = env_sensor.gas

#         # demo: use only the temperature.
#         # add others if you want.
#         if temp_value > 0:
#         #if temperature is not None:
#             value = temp_value  # temperature
#             print(f"Publishing {value} to '{IO_FEED}'.")
#             client.publish(IO_FEED, value)

#     except RuntimeError as error:
#         # Errors happen fairly often with sensors, just keep going
#         print(error.args[0])
#         time.sleep(2.0)
#         continue

#     except Exception as error:
#         raise error

#     time.sleep(SENSOR_READ_TIMEOUT)
