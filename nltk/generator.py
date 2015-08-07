#http://stackoverflow.com/questions/4858467/combining-a-tokenizer-into-a-grammar-and-parser-with-nltk

import nltk
from nltk.parse.generate import generate
from collections import defaultdict

text = nltk.word_tokenize("A car has a door.")
tags = [None,None]
tags[0] = nltk.pos_tag(text)

lines = ["This is a sentence.", "The elements of water are hydrogen and oxygen.","A dog ran.","I hope you notice me","It is in the jar."]

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
S -> NP VP  
NP -> DT NN | PRP | IN NN | NN  
VP -> VB | VP NP | VP PP
VB -> VBD | VBZ | VBP  
PP -> IN NP 
""" 
for tag, words in tag_dict.items():
    if (tag == "."):
        continue
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
sentences = list(generate(grammar, depth = 6))
shuffle(sentences)
for sentence in sentences[:20]:
    #http://www.nltk.org/howto/generate.html
    #print( "SENTENCE!!!")
    n += 1
    print(" ".join(sentence))
    #if(n>10):
    #    break

S = nltk.Nonterminal('S')
###grammar = nltk.induce_pcfg(S, allProductions)
