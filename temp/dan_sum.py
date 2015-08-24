import pickle

clusters = pickle.load(open("clusters.pickle"))
easy_search = pickle.load(open("easy_search.pickle"))


## This python script takes a cluster of tweets
##   from a txt file and
## 1) Cleans the tweets of garbled code (e.g. emojis)
## 2) Merges all tweets together into one long string
## 3) Tokenizes the sentences
##    - Some tweets have more than one sentence
##    - This is done because we are interested in 
##        generating a single sentence, which means
##        we must analyze tweets by the sentence
## 4) Tokenizes the words and tags them with parts
##      of speech tags
##    - This procedure is the most time consuming
##        out of all the processes
## 5) Determines the most common starting words of 
##      the sentences analyzed
## 6) Determines the most common pairs of starting
##      words
## 7) Generates sentences based on trigrams of words
##      and parts-of-speech tags by using common 
##      pairs of words
## 8) Randomly selects one of the sentences which uses
##      words that they share in common (which were
##      identified by the clustering algorithm)


## Regular Expressions
import re
import nltk
import random


## Tweets are in a txt file
## It is assumed that the txt file consists of
##   a single cluster
#text_read = open('onedirection_cluster.txt', 'r')


## Tweets are cleaned line by line
#text_raw = text_read.readlines()


## Tweets are grouped together by similar key words.
## These key words will be used to identify which
##   generated sentences are most representative
##   of the tweets.
## cluster_words() collects key words in a list
def cluster_words(text):
    ## key words are in the same line which begins
    ##   with the word 'cluster'
    cluster = re.compile(r'cluster')
    ## key words are in brackets
    bracket = re.compile(r"\[(.*)\]")
    for line in text:
        if cluster.match(line):
            if bracket.search(line):
                words = bracket.search(line).group(1)
                words = words.replace("'","")
                relevant_words = words.split(", ")
    print
    print "Key Words in Cluster: ", relevant_words
    print
    return relevant_words
                

## Tokenize tweets 
## Each tweet will be an element in tweet_list
def tweet_tokenizer(txt_file):
    ## Text of tweets grouped as clusters begin with info 
    ## about clusters.  We don't want cluster info in our tweet list
    cluster_info = re.compile(r'cluster')

    ## So that we can differentiate between tweets and
    ## blank lines
    legit_tweet = re.compile(r'\w')

    ## So that we can identify words in tweet
    legit_word = re.compile(r'\A\w')

    ## So that we can filter out web addresses
    ## Pattern: http then anything not a whitespace nor a boundary
    www = re.compile(r'http[^\s\b]+')

    ## So that we can separate sentences when there
    ##   is no space after period
    ## Do this after dealing with web addresses
    chardotchar = re.compile(r'([a-z])\.([A-Z])')

    ## So that we can fix ampersands
    ampersand = re.compile(r'&amp;')

    ## So that we can remove 'RT', the retweet symbol
    RT = re.compile(r'RT')

    ## So that we can remove twitter names (i.e. @TwitterName)
    name = re.compile(r'@\w+:?')

    ## So that we can remove emojis
    emoji = re.compile(r'\\[Uu]\w+\b')

    ## So that we can remove heart symbols
    heart = re.compile(r'&lt;3')
    
    ## So that we can correct 'w/' to 'with'
    ## or 'w/o' to 'without'
    ## Fix w/o befor w/
    without = re.compile(r'w/o')
    wth = re.compile(r'w/')

    ## So that we can remove hashtags that appear at end of tweet
    ## (won't use this for simple bigram sentence generator)
    hashtag_end = re.compile(r'#\w+\s*$')

    ## To create a dictionary to help identify hashtags,
    ## we will need to remove all hashtags
    ## (won't use this for simple bigram sentence generator)
    hashtag_all = re.compile(r'#.+\b')

    ## When we don't want to analyze tweets with hashtags
    ## Use this to pass tweets with hashtags stored in this list
    hashtag_any = re.compile(r'#')

    ## So that we can remove beginning or ending
    ## whitespaces after removing
    ## tokens such as 'RT' and twitter handles
    ## Should be one of last operations
    space = re.compile(r'^\s+|\s+$')

    ## So that we can add period at end if it is missing
    punctuation = re.compile(r'[\.\"!?,;:()]$')

    ## For some reason, a forwardslash often appears before 
    ## an apostrophe
    fwdslash = re.compile(r"\\\'")
    
    ## Tokenized tweets will be stored in this list
    tweet_list = []
    for lines in txt_file:
        # not a blank line, hashtagged, or cluster_info
        if legit_tweet.search(lines) and not \
           hashtag_any.search(lines) and not \
           cluster_info.match(lines): 
            clean = lines.strip('\n') # delete newline symbol
            clean = www.sub('', clean) # remove web pages
            clean = chardotchar.sub(r'\1. \2', clean) # space after '.'
            clean = emoji.sub('', clean) # remove emojis
            clean = heart.sub('', clean) # remove hearts
            clean = without.sub('without', clean) # fix w/o abbv
            clean = wth.sub('with', clean) # corrects 'with' abbv
            clean = ampersand.sub('and', clean) # fix ampersands
            clean = RT.sub('', clean) # remove 'RT'
            clean = name.sub('', clean) # removes twitter handles
            clean = space.sub('', clean) # removes spaces front/back
            clean = fwdslash.sub("\'", clean)
            if not punctuation.search(clean) and legit_tweet.search(clean):
                clean += "."
            tweet_list.append(clean)
    return tweet_list


## tweet_concatenator() merges tweets together 
##   into one long string
## Will be used to tokenize sentences as 
##  opposed to tokenizing tweets (which may
##  have more than one sentence)
def tweet_concatenator(tweet_list):
    ## If tweet ends with a space, we'll remove it
    space_at_end = re.compile(r'\s$')
    ## Identifies if tweet already has period, question mark, etc.
    punctuation_at_end = re.compile('[\.!?]$')
    #print "tweet_concatenator() . . ."
    concatenating = ""
    for element in tweet_list:
        element = element.lower() # turn everything lowercase
        if space_at_end.search(element):
            element = space_at_end.sub(r'', element)
        if punctuation_at_end.search(element):
            concatenating += element + " "
        else:
            concatenating += element + ".  "
    return concatenating


## pos_tagger() tags tokens
## The argument is a list of lists: there
##   is one list consisting of lists of individual
##   sentences where each sentence is tokenized
def pos_tagger(concatenating):
    ## So that we can differentiate between tweets and
    ## blank lines
    legit_tweet = re.compile(r'\w')
    sentences = nltk.sent_tokenize(concatenating)
    pos_list = []
    for sent in sentences:
        if legit_tweet.search(sent):
            temp_element = nltk.pos_tag(nltk.word_tokenize(sent.lower()))
            pos_list.append(temp_element)
        else:
            pos_list.append('')
    #print "POS tags: ", pos_list
    return pos_list


## Find most common first words from all tweets
## howmany parameter specifies how many first
##   words we want to later choose from
## howmany=5 means we produce the 5 most common
##   first words. 
## The function initial_pair() has a parameter
##   that determines which of the 5 most common
##   first words is used.  
## initial_pair() takes the selected word
##   and produces the five most common words
##   that follow the selected first word
## The sentence generator then takes the 
##   three most common first pair of words and
##   uses them as starting points to generate
##   sentences.
def first_word(pos_listoflist, howmany=5):
    ## For collecting first words
    first_words = []
    for element in pos_listoflist:
        if len(element) > 3: #check length of sentence
            first_words.append(element[0])
    fdist_first = nltk.FreqDist(first_words)
    #print "Common first words: ", fdist_first.most_common(howmany)
    return fdist_first.most_common(howmany)


## Finding most common initial pairs of words for sentence
## Derived only by looking at the first two words of each sentence
## Not looking at all bigrams
## Choice indicates finding more than one pair
## If choice=False, then we are returning most common pair
## init_word_rank indicates the i_th most common first word 
def initial_pair(listoflist, init_word_rank=1):
    ## The most freq first word is ranked #1 but
    ##   appears as the 0th element in the list
    ## [0] refers to the word and tag, 
    ## [1] is the number of times that word was used
    best_first_word_var = first_word(listoflist)[init_word_rank-1][0]
    #print "best first word var: ", best_first_word_var
    first_two_words_list = []
    for element in listoflist:
        #pair = [element[0], element[1]]
        # verifying the sentence has a first and second word
        if len(element) > 1: 
            pair = tuple((element[0], element[1]))
            first_two_words_list.append(pair)
    first_two_words_candidates = []
    for element in first_two_words_list:
        if element[0] == best_first_word_var:
            first_two_words_candidates.append(element)
    fdist_pair = nltk.FreqDist(first_two_words_candidates)
    # starting_pair will be a list of 5 pairs
    starting_pairs = []
    toppairs = fdist_pair.most_common(5)
    ## output needs to be a list
    for element in toppairs:
        starting_pairs.append(element[0])        
    #print "Starting Pairs:", starting_pairs
    return starting_pairs


## Trigrams are generated by sentence by
##   sentence.
## This means, for example, that no trigram 
##   will have a period as the 2nd element
## If a created trigram has a period, it 
##   will be the 3rd and last element of the
##   trigram.
## Since we are creating only one sentence,
##   we're not interested in trigrams that
##   imply that we could create more than one
##   sentence.
## Argument is a pos_listoflist
def trigrams_by_sent(listoflist):
    trigram_list = []
    for element in listoflist:
        temp_trigram = list(nltk.ngrams(element, 3))
        for element in temp_trigram:
            trigram_list.append(element)
    #print "some trigrams: ", trigram_list[:5]
    return trigram_list


## Generating sentence using trigrams without following specific sent structure
## pair_rank refers to the i_th most common initial pair desired
## working_candidates is a list of partial sentences in which
##   the function is in the process of adding more words.
## When the function adds a period to the partial sentence 
##   (or some other sentence-ending punctuation), the 
##   sentence is considered complete and is moved from 
##   working_candidates to final_candidates
def sent_generator(initial_pair, trigrams):
    ## keeps track of generated sentences
    final_candidates = []
    working_candidates = []
    ## Adding most common starting pair of words:
    working_candidates.append(initial_pair[0])
    ## Adding 2nd most common starting pair of words:
    try:
        working_candidates.append(initial_pair[1])
    except IndexError:
        pass
    ## Adding 3rd most common starting pair of words:
    try: 
        working_candidates.append(initial_pair[2])
    except IndexError:
        pass

    while len(working_candidates) > 0:
        removal_list = []
        ## Removing completed sentences from working_candidates
        for sent_candidate in working_candidates:
            if '.' in sent_candidate[-1]:
                final_candidates.append(sent_candidate)
                removal_list.append(sent_candidate)
            ## So far the length is arbitrarily set.
            ## The number refers to the number of tokens
            ##   in the partial sentence.
            ## If the partial sentence exceeds the 
            ##   set length, then it is deleted.
            elif len(sent_candidate) > 10:
                removal_list.append(sent_candidate)
        for element in removal_list:
            working_candidates.remove(element)
        ## new_candidates will be made up of the partial
        ##   sentences in working_candidates but with a 
        ##   new word added to each of the partial 
        ##   sentences
        new_candidates = []
        ## Adding words to sentences in progress
        for sent_candidate in working_candidates:
            ## ngram_candidates collects all trigram candidates
            ## All trigram candidates will have the same
            ##   first two words.
            ngram_candidates = []
            for tri_element in trigrams:
                if sent_candidate[-2] == tri_element[0] and \
                   sent_candidate[-1] == tri_element[1]:
                    ngram_candidates.append(tri_element)
            if len(ngram_candidates) > 0:
                fdist = nltk.FreqDist(ngram_candidates)
                ## Compiling two most common trigrams
                ## most_common() function still works if 
                ##   there is only one choice
                freq_ngrams = fdist.most_common(2)
                ## freq_ngrams consists of two elements
                ##   which are the two most common trigrams
                ## Each of those two elements consist of 
                ##   two other elements: the trigram AND
                ##   the number of times the trigram appears
                ##   in our tweets
                for ngram_element in freq_ngrams:
                    next_word = [] + list(sent_candidate)
                    ## [-1] is the third word of our trigram which is 
                    ##   what we want to add to our candidates
                    next_word.append(ngram_element[0][-1])
                    new_candidates.append(next_word)
        ## working_candidates is emptied, and new_candidates
        ##   will replace it
        working_candidates = []
        ## Want list of lists
        if len(new_candidates) > 0:
            working_candidates += new_candidates
            ## new_candidates must be emptied for the
            ##   next while loop
            new_candidates = []
    candidates_as_strings = []
    #print "Number of Candidates: ", len(final_candidates)
    #print "Final Candidates: " 
    for sent_tag in final_candidates:
        sent_generated = ""
        for token_tag in sent_tag:
            sent_generated += token_tag[0] + " "
        candidates_as_strings.append(sent_generated)
        #print "     " + sent_generated
    #print "Candidate list: ", candidates_as_strings
    return candidates_as_strings


## sent_by_keyword() narrows the choices of possible sentences.
## It selects sentences that use keywords that tweets
##   had in common with each other.
## After narrowing the choices, the function randomly
##   chooses one of the remaining sentences.
def sent_by_keyword(keywords, sent_choices, tweet_list):
    sent_plus_count = []
    highest_count = 0
    for sent in sent_choices:
        count = 0
        for word in keywords:
            if word in nltk.word_tokenize(sent):
                count += 1
        sent_plus_count.append((sent, count))
        if count > highest_count:
            highest_count = count
    best_sent_choices = []
    lesser_sent_choices = []
    for s_count in sent_plus_count:
        if s_count[1] == highest_count and s_count[0] not in tweet_list:
            best_sent_choices.append(s_count[0])
        elif s_count[0] not in tweet_list:
            lesser_sent_choices.append(s_count[0])
    print
    print "Best Sentence Choices Based on Key Cluster Words:"
    print best_sent_choices
    print
    if len(best_sent_choices) == 0:
        print "Best sentence choices are duplicates of analyzed tweets."
        if len(lesser_sent_choices) == 0:
            print "All generated sentences are duplicates of analyzed tweets."
        else:
            print "A randomly-chosen sentence among those which aren't duplicates of analyzed tweets:"
            print random.choice(lesser_sent_choices)
    else:
        print "Randomly-Chosen Sentence Amongst Best Sentence Choices:"
        print random.choice(best_sent_choices)

#############################################################
"""
## tweet_list is a list of tweets
tweet_list = tweet_tokenizer(["the past is good","the dog ran accross the street","everything is going just fine","the dog is great.","Another sentence about nothing.", "i went to the house","i love that movie","i think that the past is great"])
print tweet_list
## concatenated merges tweets together into one long string
## Necessary for breaking up tweets into individual sentences
concatenated = tweet_concatenator(tweet_list)

## Tagging words
pos_listoflist = pos_tagger(concatenated)

## init_word_rank determines which word to begin with.
## init_word_rank=1 selects the most common first word
initial_pairs = initial_pair(pos_listoflist, init_word_rank=1)

## trigram_list will be used to generate our sentences
## It includes words and parts-of-speech tags
trigram_list = trigrams_by_sent(pos_listoflist)

## How many tweets in cluster
print "Number of tweets analyzed: ", len(tweet_list)

print
## candidates is a list of generated sentences w/o tags
candidates = sent_generator(initial_pairs, trigram_list)
print

###Dave's extra code:
initial_pairs = initial_pair(pos_listoflist, init_word_rank=2)
candidates  += sent_generator(initial_pairs, trigram_list)

print "candidate"
print candidates

###end of Dave's extra code

## words_in_cluster is a list of words that tweets 
##   have in common
#words_in_cluster = cluster_words(text_raw)

## sent_by_keyword produces a single sentence
sent_by_keyword(["dog","great","i","past"], candidates)
"""

###Daves
###And now let's try for real

#cluster_num = 98
#print clusters[cluster_num]

def get_it_done(cluster_num):

    the_tweets = []
    for i in clusters[cluster_num]['tweet']:
        the_tweets.append(easy_search[i]['text'])

    tweet_list = tweet_tokenizer(the_tweets)
    concatenated = tweet_concatenator(tweet_list)
    pos_listoflist = pos_tagger(concatenated)
    

    trigram_list = trigrams_by_sent(pos_listoflist)
    candidates = [] #sent_generator(initial_pairs, trigram_list)
    
    for k in range(1,7):
        try:
            initial_pairs = initial_pair(pos_listoflist, init_word_rank=k)
            candidates  += sent_generator(initial_pairs, trigram_list)
        except:
            break
    
    print candidates

    sent_by_keyword(clusters[cluster_num]["keywords"], candidates, tweet_list)

get_it_done(33)
