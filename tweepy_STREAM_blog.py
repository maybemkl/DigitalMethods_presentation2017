import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import json

consumer_key = 'jG3FjTlKRU0z54iIhsiOTJkVW'
consumer_secret = 'HWdeGuaLJSViNX90RNBQKYpDEYI4t1HjiEaCRGwyVNFNBQjC0W'
access_token = '594015329-EVmuuI0Y3SPihQtnRaC726O845BtU10NPlR6kFAV'
access_secret = 'i22xOQtadddf2TUVGE4RHTBRB9BpZo9VaE5XyCMKd1ns9'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status
 
# Status() is the data model for a tweet
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse

class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('FILENAME.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True
 

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#worldwaterday'])
