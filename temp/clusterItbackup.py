import pickle
import sys 

easy_search = pickle.load(open("easy_search.pickle"))
other_inverted = pickle.load(open("other_inverted.pickle"))
#print easy_search
#print other_inverted
clusters = {}
num_clusters = 0
for num in easy_search:
    if(easy_search[num]['cluster'] != 0):
        continue
    if(easy_search[num]['text'] == 'xception'):
        continue
    #if num<7:
    #    print easy_search[num]
    num_clusters += 1
    clusters[num_clusters] = [num]
    easy_search[num]['cluster'] = num_clusters
    keywords = set(easy_search[num]['keywords'])
    while len(keywords)>0:
        nextWord = keywords.pop()
        nextTweets = other_inverted[nextWord]
        for nextNum in nextTweets:
            if(easy_search[nextNum]['cluster'] == 0):
                easy_search[nextNum]['cluster'] = num_clusters
                clusters[num_clusters].append(nextNum)
                keywords.union(set(easy_search[nextNum]['keywords']))

    #if num<7:
    #    print easy_search[num]
#print([ w for w in clusters[w] if clusters[w] > 3])

filter_it = 1
if(len(sys.argv)>1):
    filter_it = int(sys.argv[1])

for c in clusters:
    if (len(clusters[c])> filter_it):
        print "cluster number: "+ str(c)
        for d in clusters[c]:
            print easy_search[d]['text']+"\n"
        print "-------------------------------\n"
