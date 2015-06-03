import sys
import numpy as np

myDict = {}

for line in sys.stdin:
    word, num, tot_num, tf, tf_tot = line.split()
    num = int(num)
    tf = int(tf)
    tot_num = int(tot_num)
    tf_tot = int(tf_tot)

    try:
        myDict[word]['tf'] += tf
        myDict[word]['tf_tot'] += tf_tot
    except KeyError:
        myDict[word] = {'num': num, 'tot_num': tot_num, 'tf': tf, 'tf_tot': tf_tot}



tfidf_score = []
word = []
for i in myDict:
    word.append(i)
    num = float(myDict[i]['num'])
    bigN = float(myDict[i]['tf_tot'])
    smallN = float(myDict[i]['tf'])
    myLog = bigN/(smallN+1) #np.log(bigN/(smallN+1))
    tfidf_score.append(num*myLog)


out = sorted(zip(tfidf_score, word), reverse = True)
for i in out:
    print i[1], i[0]


