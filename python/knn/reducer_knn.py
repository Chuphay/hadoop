#from operator import itemgetter
import sys

#current_word = None
#current_count = 0
#word = None

if(len(sys.argv)>1):
    k = int(sys.argv[1])
else:
    k = 3

for i, line  in enumerate(sys.stdin):
    if(i >= k):
        break
    line = line.strip()
    words = line.split()
    print words[1], words[0]
    #try:
    #    count = int(count)
    #except ValueError:
    #    continue

    #if current_word == word:
    #    current_count += count
    #else:
    #    if current_word:
    #        print(current_word+"\t"+str(current_count))
    #    current_count = count
    #    current_word = word

#if current_word == word:
#    print(current_word+"\t"+str(current_count))
