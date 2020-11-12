"""
# Example of using the MQTT client class to subscribe to and publish feed values.
# Author: Tony DiCola
https://github.com/adafruit/Adafruit_IO_Python/blob/master/examples/mqtt/mqtt_client_class.py

2020-1111 PP adopted for SmartCity - Adafruit IO "MQTT dashboard"
"""

# Import standard python modules.
import random
import sys
import time

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
from lib.secrets import ADAFRUIT_IO_KEY, ADAFRUIT_IO_USERNAME

# Listening feed 
IO_FEED = 'mqtt-demofeed'

# Define callback functions which will be called
# when certain events happen.

# Connected function will be called when the client is connected to Adafruit IO.
def connected(client):
    # This is a good place to subscribe to feed changes.
    # The client parameter passed to this function is the
    # Adafruit IO MQTT client so you can make calls against it easily.
    print(f'Listening for {IO_FEED} changes...')
    # Subscribe to changes on a feed named by IO_FEED.
    client.subscribe(IO_FEED)


def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print("Disconnected from Adafruit IO!")
    sys.exit(1)


def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    print(f"Feed '{feed_id}' received new value: {payload}.")


# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

# Connect to the Adafruit IO server.
client.connect()

# Now the program needs to use a client loop function to ensure messages are
# sent and received.  There are a few options for driving the message loop,
# depending on what your program needs to do.

# The first option is to run a thread in the background so you can continue
# doing things in your program.
client.loop_background()
# Now send new values every 10 seconds.
print("Publishing a new message every 10 seconds (press Ctrl-C to quit)...")
try:
    while True:
        value = random.randint(0, 50)  # limit range so it looks like temperature
        print(f"Publishing {value} to '{IO_FEED}'.")
        client.publish(IO_FEED, value)
        time.sleep(10)
except KeyboardInterrupt:
    client.disconnect()
    print('Done')

# Another option is to pump the message loop yourself by periodically calling
# the client loop function.  Notice how the loop below changes to call loop
# continuously while still sending a new message every 10 seconds.  This is a
# good option if you don't want to or can't have a thread pumping the message
# loop in the background.
# last = 0
# print('Publishing a new message every 10 seconds (press Ctrl-C to quit)...')
# try:
#     while True:
#         # Explicitly pump the message loop.
#         client.loop()
#         # Send a new message every 10 seconds.
#         if (time.time() - last) >= 10.0:
#             value = random.randint(0, 50)
#             print(f"Publishing {value} to '{IO_FEED}'.")
#             client.publish(IO_FEED, value)
#             last = time.time()
# except KeyboardInterrupt:
#     client.disconnect()
#     print('Done')

# The last option is to just call loop_blocking.  This will run a message loop
# forever, so your program will not get past the loop_blocking call.  This is
# good for simple programs which only listen to events.  For more complex programs
# you probably need to have a background thread loop or explicit message loop like
# the two previous examples above.
#client.loop_blocking()
