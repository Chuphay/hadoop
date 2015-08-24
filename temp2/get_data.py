#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import pickle
import nltk


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
        self.data = {}


    def on_data(self, data):

        try:
            tweet = json.loads(data)['text']
            print(self.num_tweets,tweet)

        except:

            print (self.num_tweets,"exception")
            word_tokens = []


        self.num_tweets = self.num_tweets + 1
        if (self.num_tweets < 100):
            return True
        else:
            return False

    def on_error(self, status):
        pass

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    stream.filter(track=['a','e','i','o','u'], languages = ['en'])
