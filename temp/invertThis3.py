import sys 
import re
import numpy as np
import nltk


update = False
if len(sys.argv) > 1:
    if(sys.argv[1] == 'u'):
        update = True

myDict = {}
numbers = "\d+"
d = 0


myFile = open("idf_score.txt","w")
import pickle
out = pickle.load(open("idf.pickle"))
#print out

food = out["food"]
food_idf = np.log(out["daves Metadata"]/float(food))
cutoff_idf = 6 #corresponds to approximately "food"

other_inverted = {}
easy_search = {}

for line in sys.stdin:

    temp = re.search('^\((\d+), (.*)\)$', line)
    try:
        d = d+1
        num = int(temp.group(1))
        text = temp.group(2)
        text = text[2:]
        text = text[:-1]
        text = text.replace("\\n","\n")
        #print str(text)
    except AttributeError:
        print "Error"
        num = -1
        text = ""
        pass
    lower_text = text.lower()
    words = nltk.word_tokenize(lower_text)

    #tempDict = {}
    #for word in words:
    #    try:
    #        myDict[word].append(num)
    #        tempDict[word] += 1
    #    except KeyError:
    #        tempDict[word] = 1
    #        myDict[word] = [num]
    tfidfScores = []
    for word in words: #tempDict:
        try:
            myDict[word].append(num)
        except KeyError:
            myDict[word] = [num]
        tf = 1 #tempDict[word]
        try:
            df = out[word]
        except KeyError:
            df = 0
        idf = out["daves Metadata"]/float(df + 1)
        tfIdf = tf * np.log(idf)
        tfidfScores.append((tfIdf,word))

    #sorted(tfidfScores)
    tfidfScores.sort(reverse = True)
    myFile.write(text + "\n")
    myFile.write(str(num) + " ")
    easy_search[num] = {'text': text, 'keywords': [], 'cluster':0}
    for i in range(4):
        try:
            if(tfidfScores[i][0] < food_idf):
                break
            easy_search[num]['keywords'].append(tfidfScores[i][1])
            myFile.write(tfidfScores[i][1] +" "+ str(tfidfScores[i][0]) + " ")
            try:
                other_inverted[tfidfScores[i][1]].append(num)
            except KeyError:
                other_inverted[tfidfScores[i][1]] = [num]
        except IndexError:
            pass
    myFile.write("\n\n")
myFile.close()

for key in myDict:
   #print key, myDict[key]
   pass 
print out["daves Metadata"], d



#### idf

#import pickle
#out = pickle.load(open("idf.pickle"))
out["daves Metadata"] += d


for key in myDict:
    try:
        out[key] += len(set(myDict[key]))
    except KeyError:
        out[key] = len(set(myDict[key]))
    
if update:
    pickle.dump(out, open("idf.pickle", "wb"))
pickle.dump(other_inverted, open("other_inverted.pickle", "wb"))
pickle.dump(easy_search, open("easy_search.pickle", "wb"))
