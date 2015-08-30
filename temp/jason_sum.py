#http://stackoverflow.com/questions/4858467/combining-a-tokenizer-into-a-grammar-and-parser-with-nltk

import nltk
from nltk.parse.generate import generate
from collections import defaultdict
import pickle

clusters = pickle.load(open("clusters.pickle"))
easy_search = pickle.load(open("easy_search.pickle"))

cluster_num = 77
lines = []
for l in clusters[cluster_num]['tweet']:
    lines.append(easy_search[l]['text'].lower())

print lines


tag_dict = defaultdict(list)

for text in lines:
    #print (text)
    text = nltk.word_tokenize(text)
    tagged_sent = nltk.pos_tag(text)
    # Put tags and words into the dictionary
    for word, tag in tagged_sent:
        if tag not in tag_dict:
            tag_dict[tag].append(word)
        elif word not in tag_dict.get(tag):
            tag_dict[tag].append(word)

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
for tag, words in tag_dict.items():
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
    s +=  tag + " -> "
    first_word = True
    for word in words:
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
sentences = list(generate(grammar, depth = 5))
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
    #if(n>10):
    #    break
print check_this("i think i drank")
