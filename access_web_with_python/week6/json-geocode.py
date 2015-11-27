#!/usr/bin/python

import urllib
import json

srv_addr = 'http://python-data.dr-chuck.net/geojson?'

while True:
    # Read in location and validate it
    #
    # If location empty or contains 'quit' then break
    location = raw_input("Enter location: ")
    if location < 1 or location == "quit":
        break
    else:
        # Encode url to expected format for API
        #
        # Open URL and read in the data for further parsing
        url = srv_addr + urllib.urlencode({'sensor':'false', 'address': location})
        print 'Retrieving:', url
        url_conn = urllib.urlopen(url)
        urldata = url_conn.read()
        # Print retrieved number of characters
        print 'Retrieved:', len(urldata)
        # Parse the received data into a JSON string
        jsondata = json.loads(urldata)
        # Print place_id by parsing JSON data variable
        print 'Place id:', jsondata["results"][0]["place_id"]


