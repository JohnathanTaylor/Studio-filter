#importing json so we can conver the file and object into a universal format
import json
import redis
from tweet import Tweet

class TweetStore:

    #redis configuration
    redis_host = "localhost"
    redis_port = 6379
    redis_password = ""

    #tweet configuration
    #storing everything in one key 
    redis_key = "stu_tweets"
    num_tweets = 20
    trim_threshold = 100

    #creating the db connection
    def __init__(self):
        self.db = r = redis.Redis(
            host=self.redis_host,
            port=self.redis_port,
            password=self.redis_password
        )
        self.trim_count = 0

    #data is the tweet object and I push it to the head of the list
    def push(self, data):
        #pushing at the key named 'tweets'
        self.db.lpush(self.redis_key, json.dumps(data))
        self.trim_count += 1

        #periodically trim the list so it dosent grow to large
        if self.trim_count > 100:
            #at the key 'tweets' trim 0 to num_tweets  
             self.db.ltrim(self.redis_key, 0, self.num_tweets)
             self.trim_count = 0

    def tweets(self, limit=15):
        tweets = []

        #extracting out the last 15 items in the range
        for item in self.db.lrange(self.redis_key, 0, limit-1):
            #load each json and convert it to a python object
            tweet_Obj = json.loads(item)
            #creating instance of class with the data
            tweets.append(Tweet(tweet_Obj))
        #loads it to the dash borad
        return tweets