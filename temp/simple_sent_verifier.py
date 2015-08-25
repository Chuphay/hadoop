


import nltk

sent_bank = ['i run', 'he run', 'i walk', 'i walk to the store', 'he run to the store']

sample1 = 'cow jumps'

sample2 = 'he walk'
sample3 = 'i run'
samples = [sample1, sample2, sample3,"run he"]
sent_bank_tokens = []
myDict = {}
biDict = {}
myDict["tot_num_tweets"] = 0
for sent in sent_bank:
    myDict["tot_num_tweets"] += 1
    tokens = nltk.word_tokenize(sent)
    for i,word in enumerate(tokens):
        try:
            myDict[word] += 1
        except KeyError:
            myDict[word] = 1

        if(i == 0):
            try:
                biDict[("START",word)] += 1
            except KeyError:
                biDict[("START",word)] = 1
        try:
            biDict[(tokens[i-1], word)] += 1
        except KeyError:
            biDict[(tokens[i-1], word)] = 1

for s in samples:
    temp = 1
    tokens = nltk.word_tokenize(s)
    tot = myDict["tot_num_tweets"]
    for i,word in enumerate(tokens):
        try:
            temp *= float(myDict[word])/tot
        except KeyError:
            temp = 0
        if(i == 0):
            try:
                temp *= float(biDict[("START",word)])/tot
            except KeyError:
                temp *= 0.5/tot
        try:
            temp *= float(biDict[(tokens[i-1], word)])/myDict["tot_num_tweets"]
        except KeyError:
            temp *= 0.5/myDict["tot_num_tweets"]
    print s, temp



bigram_bank = []
for sent in sent_bank:
    bigram_bank.append(list(nltk.ngrams(sent.split(), 2)))



print bigram_bank
print
print biDict
