from app.TwitterSearcher import TwitterSearcher


class SearcherInterface(object):

    @staticmethod
    def search_for_search_terms_in_twitter(num_tweets, auth, terms, rt):
        """Start searching for tweets that include search terms provided as parameters, includg a RT flag to indicate
        if RTs should be included in the search results or not
        """
        searcher = TwitterSearcher()
        searcher._max_tweets = num_tweets
        searcher.create_api_instance(auth)
        searcher.search_news_org_for_terms(terms, rt)
        searcher.store_recent_tweets()



