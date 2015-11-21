#!/usr/bin/python

import urllib
from BeautifulSoup import *

sum = 0

# Open site with URLLib library
site = urllib.urlopen('http://pr4e.dr-chuck.com/tsugi/mod/python-data/data/comments_195126.html')

# Parse site via BeautifulSoup
parse_site = BeautifulSoup(site)

# Identify only the 'span' tags and add them to a list
tags = parse_site('span')

# For each item in the tags list pull out the contents, typecast to int and sum it up.
for tag in tags:
    sum += int(tag.contents[0])

# Return sum of all contents.
print sum
