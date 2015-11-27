#!/usr/bin/python
#
# Author: Adrian Arumugam
# Date: 27-November-2015

import json
import urllib
import re

while True:
    total = 0
    counter = 0
    url = raw_input("Enter URL location: ")

    # Break while loop if URL empty or quit string used 
    if len(url) < 1 or url == 'quit':
       print "URL is empty or you have chosen to quit. See-ya!"
       break
    else:
       # Retrieve URL
       print "Retrieving url:", url
       # Open URL and read data into variable
       # Print number of characters retrieved.
       openurl = urllib.urlopen(url)
       urldata = openurl.read()
       print "Retrieved:", len(urldata)

       # Parse output with json function into a dictionary
       jsondata = json.loads(urldata)
       # Search through jsondata to find all instances of 'count'
       counted = re.findall('count', str(jsondata["comments"]))

       # Loop through json dictionary
       #
       # Sum up the values produces from each count key.
       for item in jsondata["comments"]:
           total += int(item["count"])

       # Print values of count and total.
       print "Count:", len(counted)
       print "Sum:", total    
