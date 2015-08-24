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

    num_clusters += 1
    clusters[num_clusters] = {"tweet":[num]}
    easy_search[num]['cluster'] = num_clusters
    keywords = set(easy_search[num]['keywords'])
    clusters[num_clusters]["keywords"] = [k for k in keywords]
    while len(keywords)>0:
        nextWord = keywords.pop()
        nextTweets = other_inverted[nextWord]
        for nextNum in nextTweets:
            if(easy_search[nextNum]['cluster'] == 0):
                #if len(clusters[num_clusters]["tweet"]) < 10:
                #    print easy_search[nextNum]
                easy_search[nextNum]['cluster'] = num_clusters
                clusters[num_clusters]["tweet"].append(nextNum)
                new_keys = set(easy_search[nextNum]['keywords'])
                keywords.union(new_keys)
                for k in new_keys:
                    if k in clusters[num_clusters]["keywords"]:
                        continue
                    else:
                        clusters[num_clusters]["keywords"].append(k)
                #print keywords
                #clusters[num_clusters]["keywords"] = [k for k in keywords]


    #if num_clusters < 3:
    #    print easy_search[num]
    #    print clusters[num_clusters]
    #else:
    #    break


pickle.dump(clusters, open("clusters.pickle","wb"))
