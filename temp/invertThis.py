#! /usr/bin/env python

import sys
import re

myDict ={}
numbers = "\d+"

for line in sys.stdin:
    num,text = line
    words = text.split()
    for word in words:
        try:
            myDict[word].append(num)
        except KeyError:
            myDict[word] = [num]

for key in myDict:
    print key, myDict[key]
