#!/usr/bin/python

import re

# Open my file with RO permissions
content = open('regex_sum_195121.txt', 'r')

# Use regex special characters to match for numbers
# with one or more occurrences.
integers = re.findall('\d+', content.read())
sum = 0

# Loop through integers string and sum up their values
# Typecast needed to translate string value to integer.
for item in integers:
    sum += int(item)

print sum