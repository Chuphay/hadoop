import sys 
import re
import numpy as np
import pickle



update = False
init = False
if len(sys.argv) > 1:
    if(sys.argv[1] == 'u'):
        update = True
    if(sys.argv[1] == 'i'):
        init = True
        update = True

if(init):
    out = {}
    out["daves Metadata"] = 0
else:
    out = pickle.load(open("idf.pickle"))

other_inverted = {}
easy_search = {}
myDict = {}

num_tweets = 0
for line in sys.stdin:
    temp = re.search('^\((\d+), (.*)\)$', line)
    try:
        d = d+1
        num = int(temp.group(1))
        text = temp.group(2)
        text = text[2:]
        text = text[:-1]
        text = text.replace("\\n","\n")

    except AttributeError:
        print "Error"
        num = -1
        text = ""
        pass

    words = re.split(" +|\n", text)

    AnovaScores = []
    for word in words:
        try:
            myDict[word].append(num)
        except KeyError:
            myDict[word] = [num]
        tf = 1 #tempDict[word]
        try:
            df = out[word]
        except KeyError:
            df = 0
        if(init):
            pass
        else:
            idf = out["daves Metadata"]/float(df + 1)
            tfIdf = tf * np.log(idf)
            tfidfScores.append((tfIdf,word))

    #sorted(tfidfScores)
    tfidfScores.sort(reverse = True)

    easy_search[num] = {'text': text, 'keywords': [], 'cluster':0}
    for i in range(4):
        try:
            easy_search[num]['keywords'].append(tfidfScores[i][1])
            myFile.write(tfidfScores[i][1] +" "+ str(tfidfScores[i][0]) + " ")
            try:
                other_inverted[tfidfScores[i][1]].append(num)
            except KeyError:
                other_inverted[tfidfScores[i][1]] = [num]
        except IndexError:
            pass
