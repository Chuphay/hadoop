import sys 
import re

myDict = {}
numbers = "\d+"
d = 0

for line in sys.stdin:

    temp = re.search('^\((\d+), u(.*)\)$', line)
    try:
        d = d+1
        num = int(temp.group(1))
        text = str(temp.group(2))
    except AttributeError:
        print "Error"
        num = -1
        text = ""
        pass

    words = text.split()
    for word in words:
        try:
            myDict[word].append(num)
        except KeyError:
            myDict[word] = [num]

for key in myDict:
    print key, myDict[key]

#### idf

import pickle
out = {}
out["daves Metadata"] = d

for key in myDict:
    out[key] = len(set(myDict[key]))
    
pickle.dump(out, open("idf.pickle", "wb"))

