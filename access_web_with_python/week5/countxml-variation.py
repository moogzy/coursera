#!/usr/bin/python

import urllib
import xml.etree.ElementTree as ET

quit_str = 'quit'
total = 0
count_str = 0
xmlurl = raw_input('Enter XML URL: ')

# Validate whether a URL has been entered
# 
# If length is < 1 or the string 'quit' appears
# then exit the script. Otherwise continue
# with xml tree processing
if len(xmlurl) < 1 or xmlurl == quit_str:
    pass
else:
    print 'Retrieving URL: %s' % (xmlurl)
    openurl = urllib.urlopen(xmlurl)
    readxml = openurl.read()
    # Print number of characters retrieved from XML
    print 'Retrieved', len(readxml), 'characters'
    # Parse XML from a string directly into an Element.
    xmltree = ET.fromstring(readxml)
    # Use a for loop to cylce through the xml tree and find
    # all instances of the 'count' element.
    for child in xmltree.iter('count'):
       # Sum up the count element values
       total += int(child.text)
       count_str += 1

#  Print total number of count elements found
print 'Count:',count_str
# Print sum of counts
print 'Sum:',total
