#http://stackoverflow.com/questions/4858467/combining-a-tokenizer-into-a-grammar-and-parser-with-nltk

import nltk
from nltk.parse.generate import generate
import pickle
import numpy as np



clusters = pickle.load(open("clusters.pickle"))
easy_search = pickle.load(open("easy_search.pickle"))
idf = pickle.load(open("idf.pickle"))

cluster_num = 77
lines = []
for l in clusters[cluster_num]['tweet']:
    lines.append(easy_search[l]['text'].lower())


my_little_dict = {}


for text in lines:

    text = nltk.word_tokenize(text)
    tagged_sent = nltk.pos_tag(text)

    for word, tag in tagged_sent:
        if (tag == "."):
            continue
        if (tag == "``"):
            continue
        if (tag == "''"):
            continue
        if (tag == ","):
            continue
        if (tag == ":"):
            continue
        if (tag == "-NONE-"):
            continue
        if(tag ==  "PRP$"):
            tag = "PRPs"


        try:
            my_little_dict[tag][word] += 1
        except KeyError:
            try:
                my_little_dict[tag][word] = 1
            except KeyError:
                my_little_dict[tag] = {word:1}


s = """

S -> NP VP | VP NP
NP -> DT NN1 | PRP | NN1 IN | NN1 | NN1 PP | ADJP NN1 | PRPs
NN1 -> NN | NNS | NNP
VP -> VB NP | VB PP | ADVP VB | VB
ADVP -> RB 
VB -> VBZ | VBP | VBD | VBG
PP -> IN NN1
ADJP -> JJ

"""


cleaned_tags = {}
for tag in my_little_dict:
    #print tag, my_little_dict[tag]

    cleaned_tags[tag] = {}
    for word in my_little_dict[tag]:
        try:
            df = idf[word]
            #print word, df, my_little_dict[tag][word]
            word_idf = np.log(idf["daves Metadata"]/float(df))
            tf_idf = (my_little_dict[tag][word]**3)*word_idf
            #if (word_idf > filter_bottom and word_idf < filter_top):
            #not using filter, going to do a cool power tf^n_idf trick
            #as you can see up above
            try:
                cleaned_tags[tag]['tfidf'].append((tf_idf, word))
            except KeyError:
                cleaned_tags[tag]['tfidf'] = [(tf_idf, word)]
        except KeyError:
            pass


for tag in cleaned_tags:
    possibilities = sorted(cleaned_tags[tag]['tfidf'], reverse = True)
    cleaned_tags[tag]['word'] = []
    for i in range(2):
        try:
            cleaned_tags[tag]['word'].append(possibilities[i][1])
        except IndexError:
            pass


for tag in cleaned_tags:

    #if(tag ==  "PRP$"):
    #  tag = "PRPs"
    s +=  tag + " -> "
    first_word = True
    for word in cleaned_tags[tag]['word']:
        if first_word:
            s +=  "\"" + word + "\""
            first_word = False
        else:
            s += "| \"" + word + "\""
    s += "\n"

print (s)



from nltk import CFG
grammar = CFG.fromstring(s)


n = 0
from random import shuffle
sentences = list(generate(grammar, depth = 6))
shuffle(sentences)


from simple_sent_verifier import check_this, create_bigram
create_bigram(lines)

score = 0

for sentence in sentences:
    #http://www.nltk.org/howto/generate.html
    #print( "SENTENCE!!!")
    n += 1
    s = " ".join(sentence)
    temp =  check_this(s)
    if(temp>=score):
        print s, temp
        score = temp

