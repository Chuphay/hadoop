#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import pickle



#Variables that contains the user credentials to access Twitter API 
access_token = "3161805806-5knas90qzqkaLqO11HY9KwhTWKFskukj45tUocP"
access_token_secret = "m1ILxyRFwCoPHzQ55MOieoUObjXh976vz3hcgUK1a8b2G"
consumer_key = "8sOsbXSPd9ZgAzOrrktEu9nKD"
consumer_secret = "pQbOdiJEjWqVrvUFXggcoGnSD9ZgxtXnBer4Xm4RRAmdFsc1G9"


#This is a basic listener that just prints received tweets to stdout.

class StdOutListener(StreamListener):

    def __init__(self, api=None):
        super(StdOutListener, self).__init__()
        self.num_tweets = 0
        self.data = {'text':[],'pos':[],'neg':[]}


    def on_data(self, data):

        try:
            tweet = json.loads(data)['text']

            print(tweet)
            self.data['text'].append(tweet)
            positives = []
            negatives = []
            #word_tokens =  nltk.word_tokenize(tweet)

            #for word in word_tokens:
            #    if(word.lower() in pos_tokens):
            #        positives.append(word)
            #    if((word.lower() in neg_tokens)):
            #        negatives.append(word)

            #self.data['pos'].append(len(positives))
            #print('positives', self.data['pos'][-1])
            #self.data['neg'].append(len(negatives))
            #print('negatives', self.data['neg'][-1])
            #number_pos += 1
            #print(x.next())
            print('--------------------------\n')
            #f.write('-------------------------\n')
        except:

            print('--------------------------exception?\n')
            #f.write('-------------------------exception?\n')
            pass
        self.num_tweets = self.num_tweets + 1
        if (self.num_tweets < 100):
            return True
        else:
            with open('a_giant.pickle', 'wb') as handle:
                pickle.dump(self.data, handle)
            return False

    def on_error(self, status):
        print (status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    stream.filter(track=['a','the','of','me','he','she','it','is'], languages = ['en'])
