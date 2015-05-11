import sys

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

print myDict
