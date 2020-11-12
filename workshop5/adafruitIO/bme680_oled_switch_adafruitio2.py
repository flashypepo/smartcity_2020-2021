"""
'bme680_adafruitio.py'
==================================
Example of sending temperature and humidity
sensor values to an Adafruit IO feed.
Adafruit dashboard: switch for OLED/LED on or OFF

Configuration:
* Sensor: BME680 connected to i2c, address=0x77
* LED: red led connected to GPIO17
* OLED, i2c, type ssd1306, address=0x3C

PROBLEM: checking the Adafruit IO dashboard DigitalSwitch
is in the loop of about 30 minutes! So, it takes 30 minutes
before the LED and OLED reacts. Not very nice!
SOLUTION: Solve the problem yourself!

For a possible solution: bme680_oled_switch_adafruitio2.py

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

2020-1110 PP added OLED/LED switch
             in my circuit: add OLED rotate 180
2020-1104 PP new, BME680 sensor
Based upon Python code from Brent Rubell
Tutorial Link: Tutorial Link: https://learn.adafruit.com/adafruit-io-basics-temperature-and-humidity
"""
# standard python module(s)
import time

# adafruit board library (blinka).
import board
# adafruit digitalio library for LED.
import digitalio

# adafruit library for the I2C devices
from busio import I2C
# adafruit library for BME680 sensor
import adafruit_bme680

# Adafruit IO library for REST client
from Adafruit_IO import Client, Feed

# Your secret data, like Adafruit IO username and Adafruit IO key
# Remember, your key is a secret,cso make sure not 
# to publish it when you publish this code!
from lib.secrets import ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY

# custom library of BME680 view on local attached OLED display
from lib.bme680view import BMEx80View

# Delay in-between sensor readings, in seconds.
# data limit Adafruit IO: 30 data points per minute
# or in 'n' secs upload maximum 'n/2' datapoints
# Good values:
# development: 10 secs (max. 5 datapoints)
# remember: you measure ambient values, they don't change often.
# long periodes (days): 300 secs (call every 5 minutes)
# SENSOR_READ_TIMEOUT = 10  # in seconds, max 5 datapoints
SENSOR_READ_TIMEOUT = 1800  # 1x30 minuten, in seconds
# i.e 1 datapoint per graph in 30 minuten 
# -> in 10 hours: 20 datapoints per graph

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Set up Adafruit IO Feeds.
temperature_feed = aio.feeds('temperature')
humidity_feed = aio.feeds('humidity')
pressure_feed = aio.feeds('pressure')
gas_feed = aio.feeds('gas')
#TODO: altitude_feed = aio.feeds('altitude')
# feed to switch digital devices, like LED or OLED-display
digital_feed = aio.feeds('digital')

# setup environment sensor
# this case: BME680 Sensor at I2C
i2c = I2C(board.SCL, board.SDA)
BME680_I2CADDRESS = 0x77
env_sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c, BME680_I2CADDRESS)

# setup OLED-display for the environment sensor
oled = BMEx80View(i2c)

# setup red led
red_led = digitalio.DigitalInOut(board.D17)
red_led.direction = digitalio.Direction.OUTPUT


# solution to be responsive for Adafruit IO switches
# -> timed loop
# function to poweron or poweroff OLED
# depending on received value from dashboard
def wait_timeout_and_check_digital(seconds):
    """ wait for number of seconds before sending sensor
        data to Adafruit IO. While waiting, get the
        switch-value from Adafruit IO digital-feed """
    start_time = time.time()
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > seconds:
            # end of timeout
            print("start next sensor transmission ...")
            break
        # get data from Adafruit IO...
        data = aio.receive(digital_feed.key)
        #DEBUG: print(f"Received data to set LED/OLED {data.value}") # DEBUG
        # set LED (and OLED) state...
        device_state = True if data.value == "ON" else False
        # -> LED / OLED on or off...
        if device_state is True:
            oled.poweron()
            red_led.value = True
        else:
            oled.poweroff()
            red_led.value = False
        # wait a moment to avoid flooding adafruit IO...
        time.sleep(0.5)

# # set LED/OLED on/off according to received value from Adafruit IO
# def devices_onoff(value):
#     """ value: 'ON' -> OLED poweron
#         value: 'OFF' -> OLED poweroff """
#     device_state = True if value == "ON" else False
#     if device_state is True:
#         red_led.value = True
#         oled.poweron()
#         print(f"Received {value}: OLED powered on")
#     else:
#         red_led.value = False
#         oled.poweroff()
#         print(f"Received {value}: OLED powered off")


# poweroff OLED after specifed seconds
# requires: oled_show() to poweron OLED!
def oled_off_after(seconds):
    start_time = time.time()
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > seconds:
            #DEBUG: print('OLED: power off')
            oled.poweroff()
            break


def oled_show(temperature, humidity, pressure, altitude, gas):
    # power on OLED - see oled_off_after()
    oled.poweron()
    # make data dictionary for OLED-display subsystem
    # BME680: title is ignored - no room
    data = {
        "title": "BMEx80 sensor",
        "Temp": "{:0.1f} \u00b0C".format(temperature),
        "Hum": "{:0.1f} %".format(humidity),
        "Pres": "{:0.2f} hPa".format(pressure),
        "Alt": "{:0.2f} m".format(altitude),
        "Gas": "{:} Ohms".format(gas),
    }
    # DEBUG: print("sensor data\n{}".format(data))
    # show sensor data on display...
    oled.show(data)
    # 2020-1110 PP: in my case OLED display needs
    # to be rotated by 180 degree!
    # Comment code, if not necessary.
    oled.rotate_180()


""" 
BMEx80 sensor needs to be calibrated with sea level pressure,
because the altitude calculation in the sensor depends on it.
You can use the average seal level pressure (1013.25 hPa),
but the altitde is not precise enough.
It's better to use location's sea level pressure (hPa).
Location sea level pressure can be found at:
https://www.weatheronline.co.uk/weather/maps/current?LANG=en&CONT=euro&REGION=0003&LAND=NL&LEVEL=4&R=310&CEL=C&ART=tabelle&TYP=druck
I use 'Amsterdam/Schiphol' sea level value.
"""
def calibrate(value):
    print(f"... BME680 sensor calibrating for sea level pressure: {value}")
    env_sensor.sea_level_pressure = value
    assert env_sensor.sea_level_pressure == value


calibrate(1025)  # 10 Nov 2020 19:00

# main loop
print("Press CTRL-C to exit...")
while True:
    try:
        # receive switch-value for LED/OLED
        # solution #1: does not work nicely.
        # -> solution #2: take reading outside loop
        # data = aio.receive(digital_feed.key)
        # devices_onoff(data.value)  # pass an value

        # send to adafruit IO feeds the barometric values
        # get sensor values
        temperature = env_sensor.temperature
        humidity = env_sensor.humidity
        pressure = env_sensor.pressure
        altitude = env_sensor.altitude
        gas = env_sensor.gas

        if humidity is not None \
            and temperature is not None:
            # show on console
            print('Temperature={0:0.1f}\u00b0C\tHumidity={1:0.1f}%\tPressure={2:0.1f}hPa'.format(temperature, humidity, pressure))
            print('Altitude   ={0:0.1f} m\tGas={1:} Ohm'.format(altitude, gas))
            # show on oled
            oled_show(temperature, humidity, pressure, altitude, gas)

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
    print(f'waiting {SENSOR_READ_TIMEOUT} seconds...')
    oled_off_after(10)  # turnoff OLED after 10 seconds

    # solution #2: check aio digital feed in 
    # my sleep function and return if
    # SENSOR_READ_TIMEOUT is passed
    # time.sleep(SENSOR_READ_TIMEOUT)
    wait_timeout_and_check_digital(SENSOR_READ_TIMEOUT)
