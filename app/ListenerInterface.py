from tweepy import Stream
from app.TwitterListener import TwitterListener


class ListenerInterface(object):

    @staticmethod
    def get_live_tweets_from_twitter_stream(auth, terms, num_tweets):
        """Start collecting tweets from the live Twitter stream that include search terms provided as parameters"""
        listener = TwitterListener()
        listener._max_tweets = num_tweets
        twitter_stream = Stream(auth, listener)
        twitter_stream.filter(track=[terms], languages=['en'])
        listener.store_live_tweets()

