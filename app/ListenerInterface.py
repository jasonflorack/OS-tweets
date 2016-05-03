from tweepy import Stream
from app.TwitterListener import TwitterListener


class ListenerInterface:

    # Start collecting tweets from the live Twitter stream that include search terms provided as parameters
    @staticmethod
    def get_live_tweets_from_twitter_stream(auth, terms, num_tweets):
        listener = TwitterListener()
        listener.set_max_tweets(num_tweets)
        twitter_stream = Stream(auth, listener)
        twitter_stream.filter(track=terms, languages=['en'])
        listener.store_live_tweets()

