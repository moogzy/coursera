#!/usr/bin/python

import re

content = open('regex_sum_42.txt', 'r')
integers = re.findall('\d+', content.read())
sum = 0

for item in integers:
    sum += int(item)

print sum