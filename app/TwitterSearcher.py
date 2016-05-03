import tweepy


class TwitterSearcher:

    def __init__(self):
        super(TwitterSearcher, self).__init__()
        self.__api = None
        self.__max_tweets = 0
        self.__tweets_collected = 0
        self.__tweet_cache = None
        self.__all_found_tweets_json = {}

    # Set the maximum number of tweets for the search
    def set_max_tweets(self, maximum):
        self.__max_tweets = int(maximum)

    # Create API instance
    def create_api_instance(self, auth):
        self.__api = tweepy.API(auth)

    # Set search query with terms and the RT flag if desired, then start the search
    def search_news_org_for_terms(self, terms, rt):
        query = terms
        if int(rt) == 0:
            query += " -filter:retweets"
        self.search_twitter_and_collect_tweets(query)

    # Search Twitter and present tweets that match the search criteria
    def search_twitter_and_collect_tweets(self, query):
        # Instantiate Tweepy Cursor object to conduct search
        self.__tweet_cache = tweepy.Cursor(self.__api.search, q=query, lang='en')
        if self.__tweet_cache:
            # Present search result tweets to user
            print()
            if self.__max_tweets == 1:
                print("Here is a tweet that met the search criteria:")
            else:
                print("Here are tweets that met the search criteria:")
            print()
            for tweet in self.__tweet_cache.items(self.__max_tweets):
                print("{0})".format(str(self.__tweets_collected + 1)))
                print("{0}".format(tweet.text))
                print("User:      {0} (@{1})".format(tweet.user.name, tweet.user.screen_name))
                print("Retweeted: {0} times".format(tweet.retweet_count))
                print("Favorited: {0} times".format(tweet.favorite_count))
                print("Created:   {0}".format(tweet.created_at))
                print("-----------------------------------------------------------------------------------------------")
                # Save the id_str of each tweet that comes in, in case the user wants to access the tweet via web
                self.__all_found_tweets_json['Tweet' + str(self.__tweets_collected+1)] = tweet.id_str
                self.__tweets_collected += 1

    # Store the id strings (id_str) of the recent tweets found in the search, in case the user wants to
    # view the tweet via the web
    def store_recent_tweets(self):
        if len(self.__all_found_tweets_json) != 0:
            try:
                with open('app/data/election.json', 'w') as f:
                    f.write('{')
                    for x in range(1, len(self.__all_found_tweets_json)):
                        this_tweet = 'Tweet{0}'.format(x)
                        f.write('"' + this_tweet + '":{"id_str":' + self.__all_found_tweets_json[this_tweet] + '},')
                    last_tweet = 'Tweet{0}'.format(len(self.__all_found_tweets_json))
                    f.write('"' + last_tweet + '":{"id_str":' + self.__all_found_tweets_json[last_tweet] + '}}')
                    f.close()
                    return True
            except BaseException as e:
                print("Error in TwitterSearcher's store_recent_tweets method: {0}".format(str(e)))
