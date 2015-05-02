#! /usr/bin/env python

import sys 

for line in sys.stdin:
    # first we want to remove the leading and trailing whitespaces 
    line = line.strip()
    # now we split the line into words
    words = line.split()
    # now we format the way mapreduce works in java 
    for word in words:
        print '%s \t %s' %(word, 1)
