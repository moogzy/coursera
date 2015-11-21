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
    # Parse XML into a string
    xmltree = ET.fromstring(readxml)
    # Search XML string for all occurrences of 'count' element
    counts = xmltree.findall('.//count')
    # Print count of 'count' elements
    print 'Count:', len(counts)
    # Use while loop to check against a counter string
    # Only run when counter string is less than the length of counts
    while count_str < len(counts):
        # Sum up the total value of all counts from the xml tree
        total += int(counts[count_str].text)
        count_str += 1

# Print sum of counts
print 'Sum:',total
