"""
test programa voor DHT11-sensor

Connections DHT11 sensor:
    Signal -> GPIO10
    GND -> GND, +Vcc -> 3V3.

Dependencies:
1. adafruit blinka
    'pip3 install adafruit-blinka'
2. adafruit DHT library
    'pip3 install adafruit-circuitpython-dht'
3. package 'libgpiod2'
    'sudo apt-get install libgpiod2'
NB. vergeet niet eerst Raspberry PI bij te werken:
    'sudo apt update; sudo apt upgrade'

2020-1104 PP new, based upon [Source] Python Setup
             but with DHT11 sensor
[Source] https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging
"""
import time
import adafruit_dht
import board

# initialize DHT11-sensor on GPIO10
dht_device = adafruit_dht.DHT11(board.D10)

while True:
    try:
        # get the sensor values
        temperature_c = dht_device.temperature
        humidity = dht_device.humidity
        if temperature_c is not None \
        and humidity is not None:
            # print values in console
            print(f"Temperatuur: {temperature_c}\u00b0C", end='\t')
            print(f"Luchtvochtigheid: {humidity}%")

    except RuntimeError as error:
        # Errors happen fairly often, 
        # DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dht_device.exit()
        raise error
 
    # wait for next reading, at least 2 seconds
    time.sleep(2.0)
