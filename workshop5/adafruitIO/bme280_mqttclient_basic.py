"""
`bmx80_mqttclient.py`
---------------------------------------------------------
Example of reading and writing using MQTTClient
Author: Tony DiCola
https://github.com/adafruit/Adafruit_IO_Python/blob/master/examples/mqtt/mqtt_client_class.py

2020-1112 PP TODO: message() wordt niet aangeroepen(?)
2020-1105 PP adopted mqtt_basic.py for an environment sensor (BMEx80)
"""
# Import standard python modules.
import sys
import time

# import adafruit board library (blinka).
import board
# import adafruit i2c library (blinka).
from busio import I2C
# import adafruit bmex80 library (blinka).
#import adafruit_bme680
import adafruit_bme280

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

# setup environment sensor
# this case: BME280 Sensor on I2C
i2c = I2C(board.SCL, board.SDA)
BME280_I2CADDRESS = 0x76  # commandline: i2cdetect -y 1
env_sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, BME280_I2CADDRESS)


# Define callback functions which will be called when certain events happen.
def connected(client):
    """Connected function will be called 
       when the client connects.
    """
    client.subscribe(IO_FEED)
    print(f"connected(): Listen/subscribed to '{IO_FEED}'.")


def disconnected(client):
    """Disconnected function will be called
       when the client disconnects.
    """
    print('disconnected(): disconnected from Adafruit IO!')
    sys.exit(1)


def message(client, feed_id, payload):
    """Message function will be called when a subscribed feed 
       has a new value.
       The feed_id parameter identifies the feed, 
       and the payload parameter has the new value.
    """
    print(f"Feed '{feed_id}' received new value: {payload}")


# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect       =   connected
client.on_disconnect    =   disconnected
client.on_message       =   message

# Connect to the Adafruit IO server.
client.connect()

# keep running in the background...
client.loop_background()

print(f'Publishing a new message every {SENSOR_READ_TIMEOUT} seconds (press Ctrl-C to quit)...')
while True:
    try:
        # demo: use only the temperature.
        temperature = env_sensor.temperature
        # humidity = env_sensor.humidity
        # pressure = env_sensor.pressure
        value = temperature
        if value is not None:
            print(f"Publishing {value} to '{IO_FEED}'.")
            client.publish(IO_FEED, value)

    except RuntimeError as error:
        # Errors happen fairly often with sensors, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue

    except Exception as error:
        raise error
    # sleep until next time...
    time.sleep(SENSOR_READ_TIMEOUT)
