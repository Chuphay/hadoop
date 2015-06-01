import sys
import os
import re

file_name = os.environ['mapreduce_map_input_file']
file_start = os.environ['mapreduce_map_input_start']
file_length = os.environ['mapreduce_map_input_length']

myDict = {}
for line in sys.stdin:
    words = [i for i in re.split(r'\W+',line.lower()) if i]
    for word in words:
        try:
            myDict[word] += 1
        except KeyError:
            myDict[word] = 1

for word in myDict:
    print word, file_name, myDict[word]
