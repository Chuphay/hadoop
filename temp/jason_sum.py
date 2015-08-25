#http://stackoverflow.com/questions/4858467/combining-a-tokenizer-into-a-grammar-and-parser-with-nltk

import nltk
from nltk.parse.generate import generate
from collections import defaultdict

text = nltk.word_tokenize("A car has a door.")
tags = [None,None]
tags[0] = nltk.pos_tag(text)

#myFile = open("text.txt").readlines()

lines = ["This is a long sentence.", "I love One direction", "The elements of water are hydrogen and oxygen.","the fat dog slowly ran.","I hope you did not notice me","It is in the jar.", "the boy quickly skipped across the frozen pond", "today I went to the grocery store for a dozen eggs", "I like to eat potatoes while riding a red bike", "i do not have any plans for monday yet", "I saw the cute boy I like but I do not think he saw me", "I have too much time on my small hands"]

tag_dict = defaultdict(list)

for text in lines:
    print (text)
    text = nltk.word_tokenize(text)
    tagged_sent = nltk.pos_tag(text)
    # Put tags and words into the dictionary
    for word, tag in tagged_sent:
        if tag not in tag_dict:
            tag_dict[tag].append(word)
        elif word not in tag_dict.get(tag):
            tag_dict[tag].append(word)

#print tags
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

for sentence in sentences[:10]:
    #http://www.nltk.org/howto/generate.html
    #print( "SENTENCE!!!")
    n += 1
    print(" ".join(sentence))
    #if(n>10):
    #    break

