import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
import json

consumer_key = YOUR_KEY
consumer_secret = YOUR_SECRET
access_token = YOUR_ACCESS_TOKEN
access_secret = YOUR_ACCESS_SECRET
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status
 
# Status() is the data model for a twee
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse

class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('ExijoAMiPAHrlamento.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True
 

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#StopBlackstone'])
