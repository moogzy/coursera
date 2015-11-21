#!/usr/bin/python

import urllib
from BeautifulSoup import *

# Initialize variables
url = raw_input('Enter URL: ')
count = int(raw_input('Enter count: '))
pos = int(raw_input('Enter position: '))
instance = 0
url_str = ' URL: %s'

# While loop to measure against the given count.
while instance < count:
    print 'Retrieving' + url_str % (url)

    # Create html variable which holds retrieved URL then
    # pass it through BeautifulSoup.
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
    
    # Extract anchor tags from soup variable.
    tags = soup('a')
    # Extract the url to follow from the given position minus 1(count
    # starts from 0).
    url = tags[pos - 1].get('href', None)

    # Increase instance by one to ensure we don't end up with infinite loop.
    instance += 1

# Print the last url retrieved once exiting the while loop.
print 'Last' + url_str % (url)

