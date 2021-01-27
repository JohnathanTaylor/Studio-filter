import tweepy
import datetime
from textblob import TextBlob
from tweet_store import TweetStore
import json

file_path = "../config/api.json"

with open(file_path) as f:
    twitter_api = json.loads(f.read())

#access key value pairs
consumer_key = twitter_api['consumer_key']
consumer_secret = twitter_api['consumer_secret']
access_token = twitter_api['access_token']
access_token_secret = twitter_api['access_token_secret']

#authenticates tweepy and twittter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#creating a new API object and feed it our auth
api = tweepy.API(auth)

#creating a new instance of tweetstore class
store = TweetStore()

#setting up the listener of our own by ovveriding tweepys
class StreamListener(tweepy.StreamListener):

    def on_status(self, status):

        if ('RT @' not in status.text):
            #created a new textblob object which provides certain methods and we put in the tweet text
            blob = TextBlob(status.text)
            #extract out the sentiment which also extends a couple methods
            sent = blob.sentiment
            #extract out the polarity value and subjectivity
            polarity = sent.polarity
            subjectivity = sent.subjectivity

            tweet_item = {
                'id_str': status.id_str,
                'text': status.text,
                'polarity': polarity,
                'subjectivity': subjectivity,
                'username': status.user.screen_name,
                'name': status.user.name,
                'profile_image_url': status.user.profile_image_url,
                'received': datetime.datetime.now().strftime("%Y-%m-%d %h:%M:%S")
            }
            #pushing the item to redis
            store.push(tweet_item)
            print("Pushed to redis: ", tweet_item)
    
    def on_error(self, status_code):
        #if we're being rate limited stop
        if status_code == 420:
            return False

#creating an instance of our stream listener class
stream_listener = StreamListener()
#pass in it the auth credentials the pass in the stream lsitener
stream = tweepy.Stream(auth = api.auth, listener = stream_listener)
#doing a filter passing in a list of terms instead of the whole feed
stream.filter(track=["StudioBones", "Madhouse", "@WIT_STUDIO", "Witstudio", "Studioghibli", 
"sunrisestudio", "studiomappa", "MAPPA"])  
