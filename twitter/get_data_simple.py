import tweepy

#Variables that contains the user credentials to access Twitter API 
access_token = "3161805806-5knas90qzqkaLqO11HY9KwhTWKFskukj45tUocP"
access_token_secret = "m1ILxyRFwCoPHzQ55MOieoUObjXh976vz3hcgUK1a8b2G"
consumer_key = "8sOsbXSPd9ZgAzOrrktEu9nKD"
consumer_secret = "pQbOdiJEjWqVrvUFXggcoGnSD9ZgxtXnBer4Xm4RRAmdFsc1G9"

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)

#myStreamListener = MyStreamListener()
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
myStream = tweepy.Stream(auth = auth, listener=MyStreamListener())

myStream.filter(track=['python'])
