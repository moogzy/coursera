#!/usr/bin/python

import socket
import re

# Create socke and open socket to pythonlearn.com
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect(('www.pythonlearn.com', 80))
mysock.send('GET http://www.pythonlearn.com/code/intro-short.txt HTTP/1.0\n\n')

# Receive data from socket.
#
# Break when no data received.
# Search for headers and print out header items in list.
while True:
    data = mysock.recv(512)
    if ( len(data) < 1 ) :
        break
    headers = re.findall('\S+: .*', data)
    for item in headers:
    	print item

# Cleanup socket.
mysock.close()