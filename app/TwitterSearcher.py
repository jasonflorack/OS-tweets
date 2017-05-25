import tweepy


class TwitterSearcher(object):

    def __init__(self):
        super(TwitterSearcher, self).__init__()
        self._api = None
        self._max_tweets = 0
        self._tweets_collected = 0
        self._tweet_cache = None
        self._all_found_tweets_json = {}

    @property
    def max_tweets(self):
        return self._max_tweets

    @max_tweets.setter
    def max_tweets(self, maximum):
        self._max_tweets = int(maximum)

    def create_api_instance(self, auth):
        """Create API instance"""
        self._api = tweepy.API(auth)

    def search_news_org_for_terms(self, terms, rt):
        """Set search query with terms and the RT flag if desired, then start the search"""
        query = terms
        if int(rt) == 0:
            query += " -filter:retweets"
        query = [query]
        self.search_twitter_and_collect_tweets(query)

    def search_twitter_and_collect_tweets(self, query):
        """Search Twitter and present tweets that match the search criteria"""
        # Instantiate Tweepy Cursor object to conduct search
        self._tweet_cache = tweepy.Cursor(self._api.search, q=query, lang='en')
        if self._tweet_cache:
            # Present search result tweets to user
            print('')
            if self._max_tweets == 1:
                print("Here is a tweet that met the search criteria:")
            else:
                print("Here are tweets that met the search criteria:")
            print('')
            for tweet in self._tweet_cache.items(int(self._max_tweets)):
                print("{0})".format(str(self._tweets_collected + 1)))
                print("{0}".format(tweet.text.encode('UTF-8')))
                print("User:      {0} (@{1})".format(tweet.user.name.encode('UTF-8'), tweet.user.screen_name.encode('UTF-8')))
                print("Retweeted: {0} times".format(tweet.retweet_count))
                print("Favorited: {0} times".format(tweet.favorite_count))
                print("Created:   {0}".format(tweet.created_at))
                print("-----------------------------------------------------------------------------------------------")
                # Save the id_str of each tweet that comes in, in case the user wants to access the tweet via web
                self._all_found_tweets_json['Tweet' + str(self._tweets_collected+1)] = tweet.id_str
                self._tweets_collected += 1

    def store_recent_tweets(self):
        """Store the id strings (id_str) of the recent tweets found in the search, in case the user wants to
        view the tweet via the web
        """
        if len(self._all_found_tweets_json) != 0:
            try:
                with open('app/data/election.json', 'w') as f:
                    f.write('{')
                    for x in range(1, len(self._all_found_tweets_json)):
                        this_tweet = 'Tweet{0}'.format(x)
                        f.write('"' + this_tweet + '":{"id_str":' + self._all_found_tweets_json[this_tweet] + '},')
                    last_tweet = 'Tweet{0}'.format(len(self._all_found_tweets_json))
                    f.write('"' + last_tweet + '":{"id_str":' + self._all_found_tweets_json[last_tweet] + '}}')
                    f.close()
                    return True
            except BaseException as e:
                print("Error in TwitterSearcher's store_recent_tweets method: {0}".format(str(e)))
