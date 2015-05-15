import sys
import re

if(len(sys.argv) != 2):
    print "Proper usage: python tfidf_mapper.py textfile.txt"
    sys.exit(1)

myFile = open(sys.argv[1]).read()
words = [i for i in re.split(r'\W+',myFile.lower()) if i]
myWords = {}
for word in words:
    try:
        myWords[word]['num'] += 1
    except KeyError:
        myWords[word] = {'num': 1, 'tf': 0}

#print myWords

total = 0
for line in sys.stdin:
    internal_words = line.split()
    internal_numbers = [int(myNum) for i, myNum in enumerate(internal_words[1:]) if i%2 == 1]
    l = sum(internal_numbers)
    total += l
    try:
        myWords[internal_words[0]]['tf'] = l
    except KeyError:
        pass

l = len(words)
for i in myWords:
    print i, myWords[i]['num'], l, myWords[i]['tf'], total
