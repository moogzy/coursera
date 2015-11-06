#!/usr/bin/python

import re

# Compact version 
# Open file, read, regex search for integers, typecast to integer
# Sum value of integers
print sum([int(i) for i in re.findall('[0-9]+',open('regex_sum_195121.txt','r').read())])