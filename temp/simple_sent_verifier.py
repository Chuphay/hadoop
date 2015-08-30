import nltk



myDict = {}
biDict = {}
def create_bigram(sent_bank):
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

def check_this(s):
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
                temp *= 0.1/tot
        try:
            temp *= float(biDict[(tokens[i-1], word)])/myDict["tot_num_tweets"]
        except KeyError:
            temp *= 0.1/myDict["tot_num_tweets"]
    return temp*len(tokens)


if __name__ == "__main__":
    print "here"
    sent_bank = ['i run', 'he run', 'i walk', 'i walk to the store', 'he run to the store']

    sample1 = 'cow jumps'

    sample2 = 'he walk'
    sample3 = 'i run'
    samples = [sample1, sample2, sample3,"run he"]
    create_bigram(sent_bank)
    check_this(sample2)
    
