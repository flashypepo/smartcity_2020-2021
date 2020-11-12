#!/home/pi/.virtualenvs/blinka/bin/python
"""
Starwars banner

Usage:
Execute in a terminal with command: ./starwars.py 

Notes:
File starwars.py must have eXecute mode 
   $ chmod +x starwars.py 
It doesn't work at Windesheim (websocket port 23 closed)

2020-11-03 PP updated for Raspberry PI
2019 PP smart devices - sample code for websockets example
"""
import socket

# get address information of site
url = 'towel.blinkenlights.nl'
addr_info = socket.getaddrinfo(url, 23)

# get IP and port
# 2020-1103 PP changed for Raspberry PI
# addr = addr_info[0][-1]
addr = addr_info[5][4]

# connect to it via socket
s = socket.socket()
s.connect(addr)

# print content/animation in console
# use Ctrl-C to interrupt
while True:
    data = s.recv(500)
    print(str(data, 'utf8'), end='')
