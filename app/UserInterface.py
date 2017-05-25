import os
import webbrowser
import json
from app.ListenerInterface import ListenerInterface
from app.SearcherInterface import SearcherInterface


class UserInterface(object):
    def __init__(self):
        super(UserInterface, self).__init__()
        self._auth = None
        self._search_terms = ''
        self._num_tweets = None
        self._incl_retweets = 0
        self._news_org = None
        self._search_term_dict = {1: '#Election2016',
                                   2: ['Hillary', 'Clinton', '#ImWithHer', '#HillaryClinton', '#Hillary2016'],
                                   3: ['Donald Trump', 'Trump', '#MakeAmericaGreatAgain', '#Trump', '#trumptrain',
                                       '#donaldtrump', '#Trump2016'],
                                   4: ['Bernie', 'Sanders', '#Bernie2016', '#berniesanders', '#feelthebern'],
                                   5: ['Ted Cruz', 'Cruz', '#ChooseCruz', '#tedcruz', '#cruz', '#CruzFiorina2016',
                                       '#Cruz2016'],
                                   6: ['John Kasich', '#JohnKasich', '#Kasich2016', '#Kasich4Us', 'Kasich'],
                                   7: ['Democrat', 'Democrats', '#democrat', '#left', '#Democratic', '#liberal'],
                                   8: ['Republican', 'Republicans', '#GOP', '#Republican', '#rightwing',
                                       '#conservative']}
        self._news_org_dict = {1: 'nytimes', 2: 'CNN', 3: 'WSJ', 4: 'TIME', 5: 'FoxNews',
                                6: 'washingtonpost', 7: 'ABC', 8: 'CBSNews', 9: 'NBCNews', 10: 'Newsweek'}

    @property
    def auth(self):
        return self._auth

    @auth.setter
    def auth(self, auth):
        self._auth = auth

    @property
    def search_terms(self):
        return self._search_terms

    @search_terms.setter
    def search_terms(self, search_terms):
        self._search_terms = search_terms

    @property
    def num_tweets(self):
        return self._num_tweets

    @num_tweets.setter
    def num_tweets(self, num_tweets):
        self._num_tweets = num_tweets

    @property
    def incl_retweets(self):
        return self._incl_retweets

    @incl_retweets.setter
    def incl_retweets(self, incl_retweets):
        self._incl_retweets = incl_retweets

    @property
    def news_org(self):
        return self._news_org

    @news_org.setter
    def news_org(self, news_org):
        self._news_org = news_org

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def greeting():
        print("******************************************************************************************************")
        print('                                  Election 2016 Twitter Tracker')
        print("******************************************************************************************************")
        print('This app uses the Twitter API (often via Tweepy) to search for tweets related to the 2016 US')
        print('Presidential Election.  The search can be done either from the recent past, or from the live Twitter')
        print('Stream. After a search is completed, you will be presented the tweets that met the search criteria,')
        print('along with an option to view one or more of the tweets in your browser.')

    def pick_recent_or_live_tweets(self):
        print('')
        print('OPTIONS:')
        print('--------')
        print('1) Search for recent news-oriented Election 2016 tweets')
        print('2) Collect live Election 2016 tweets from the Twitter stream')
        print('')
        choice = raw_input('PICK 1 or 2: ')
        self.handle_recent_or_live_choice(choice)

    def handle_recent_or_live_choice(self, choice):
        """Take in the user's choice from the top menu and handle it accordingly."""
        if choice == '1':
            self.ask_for_org()
            self.present_search_term_options()
            self.ask_for_search_terms(org=self._news_org)
            self.ask_num_tweets_search()
            self.activate_news_org_search(self._num_tweets)
        elif choice == '2':
            print('')
            print("You chose to collect live tweets concerning Election 2016.")
            self.present_search_term_options()
            self.ask_for_search_terms(org=None)
            self.ask_num_tweets_live()
            self.activate_stream_listener(self._num_tweets)
        else:
            self.invalid_choice()

    def invalid_choice(self):
        """Handle an invalid choice off of the main menu."""
        new_choice = raw_input('Invalid choice.  Please select 1 or 2: ')
        self.handle_recent_or_live_choice(new_choice)

    @staticmethod
    def present_search_term_options():
        """Present user with terms that can be included in the Twitter search

        Method for RECENT or LIVE tweets
        """
        print('')
        print("Here are eight groups of terms related to the 2016 US Presidential Election:")
        print("1) #Election2016")
        print("2) Hillary, Clinton, #ImWithHer, #HillaryClinton, #Hillary2016")
        print("3) 'Donald Trump', Trump, #MakeAmericaGreatAgain, #Trump, #trumptrain, #donaldtrump, "
              "#Trump2016")
        print("4) Bernie, Sanders, #Bernie2016, #berniesanders, #feelthebern")
        print("5) 'Ted Cruz', Cruz, #ChooseCruz, #tedcruz, #cruz, #CruzFiorina2016, #Cruz2016")
        print("6) 'John Kasich', Kasich, #JohnKasich, #Kasich2016, #Kasich4Us")
        print("7) Democrat, Democrats, #democrat, #left, #Democratic, #liberal")
        print("8) Republican, Republicans, #GOP, #Republican, #rightwing, #conservative")

    def ask_for_search_terms(self, org):
        """Ask user which search term they want to use, and set their choice

        Method for RECENT or LIVE tweets
        """
        print('')
        term = raw_input('Which term do you want to add to the search?  Pick one: ')
        # Handle invalid responses
        while not term.isdigit() or '-' in term or int(term) > 8 or int(term) <= 0:
            term = raw_input('Invalid choice. '
                             'Please enter a digit corresponding to the search term you want to add to the search: ')
        # User response is accepted; pick search term from the search_term_dict
        search_term = self._search_term_dict[int(term)]
        # Create search string and store in self._search_terms variable
        if type(search_term) is list and org:
            for term in search_term[:-1]:
                self._search_terms = self._search_terms + term + ' ' + org + ' OR '
            self._search_terms = self._search_terms + search_term[-1] + ' ' + org
        else:
            self._search_terms = search_term

    def ask_for_org(self):
        """Ask user which news organization they want to include as a search term

        Method for RECENT tweets only
        """
        print('')
        print('You chose to search for recent news-oriented Election 2016 tweets. In order to increase the chance')
        print('that quality content will be found, the search will look specifically for tweets that mention a ')
        print('popular news organization, or are from a news organization.')
        print('')
        print("Here are ten top news organizations you can include in the search:")
        print("1) The New York Times")
        print("2) CNN")
        print("3) Wall Street Journal")
        print("4) TIME.com")
        print("5) Fox News")
        print("6) Washington Post")
        print("7) ABC News")
        print("8) CBS News")
        print("9) NBC News")
        print("10) Newsweek")
        print('')
        org_id = raw_input('Which news organization do you want (enter number)? ')
        # Handle invalid responses
        while not org_id.isdigit() or '-' in org_id or int(org_id) > 10 or int(org_id) <= 0:
            org_id = raw_input('Invalid choice.'
                               'Please enter a digit corresponding to the news organization '
                               'you want to include in the search: ')
        # User response is accepted; pick news organization's Twitter username from news_org_dict
        news_org = self._news_org_dict[int(org_id)]
        # Store selected news organization's Twitter username
        self._news_org = news_org

    def ask_num_tweets_search(self):
        """Ask user how many tweets to search for

        Method for RECENT tweets only
        """
        print('')
        tweets_wanted = raw_input('How many election-related tweets do you want to obtain that are from, '
                                  'or mention, @{0} (MAX=100)? '.format(self._news_org))
        # Handle invalid responses
        while not tweets_wanted.isdigit() or not 0 < int(tweets_wanted) < 101:
            tweets_wanted = raw_input('Invalid choice. Please enter a digit between 1 and 100: ')
        # Store user's desired number of tweets
        self._num_tweets = tweets_wanted
        # Ask user if they want to include RTs or not
        incl_retweets = raw_input('Include retweets (enter Y or N)? ')
        # Handle invalid responses
        while incl_retweets != 'y' and incl_retweets != 'n' and incl_retweets != 'Y' and incl_retweets != 'N':
            incl_retweets = raw_input('Invalid response. Please enter Y for yes or N for no: ')
        # If user elects to include RTs in the search, set the appropriate variable which will flag this in the search
        if incl_retweets == 'y' or incl_retweets == 'Y':
            self._incl_retweets = 1

    def ask_num_tweets_live(self):
        """Ask user how many tweets to collect from the live Twitter stream

        Method for LIVE tweets only
        """
        print('')
        tweets_wanted = raw_input('How many tweets do you want to collect (MAX=100)? ')
        # Handle invalid responses
        while not tweets_wanted.isdigit() or not 0 < int(tweets_wanted) < 101:
            tweets_wanted = raw_input('Invalid response. Please enter a digit between 1 and 100: ')
        # Store user's desired number of tweets
        self._num_tweets = tweets_wanted

    def activate_news_org_search(self, num_tweets):
        """Send num_tweets, auth, search terms, and the include retweets setting to a SearcherInterface which will
        set up the search

        Method for RECENT tweets only
        """
        searcher = SearcherInterface()
        searcher.search_for_search_terms_in_twitter(num_tweets, self._auth, self._search_terms, self._incl_retweets)

    def activate_stream_listener(self, num_tweets):
        """Send auth, search terms, and the number of tweets the user wants over to a ListenerInterface which will
        set up the Twitter Stream listener

        Method for LIVE tweets only
        """
        listener = ListenerInterface()
        listener.get_live_tweets_from_twitter_stream(self._auth, self._search_terms, num_tweets)

    def view_tweet_in_browser_or_end_program(self):
        """After the search is done and the tweets are presented to the user,
        ask user if s/he wants to view one of the listed tweets on the web via their browser
        """
        loop = 0
        while loop >= 0:
            loop += 1
            print('')
            # Use slightly different wording in the question after the first time it's asked
            if loop == 1:
                response = raw_input('Do you want to view a tweet listed above via your web browser (enter Y or N)? ')
            else:
                response = raw_input('Do you want to view another tweet from the search results (enter Y or N)? ')
            # Handle invalid responses
            while response != 'y' and response != 'n' and response != 'Y' and response != 'N':
                response = raw_input('Invalid response.  Please enter Y for yes or N for no: ')
            # Handle a YES response
            if response == 'Y' or response == 'y':
                line_of_tweet = raw_input('What is the line number of the tweet with the desired URL? ')
                # Handle invalid responses
                while not line_of_tweet.isdigit() or \
                        int(line_of_tweet) > int(self._num_tweets) or \
                        int(line_of_tweet) <= 0:
                    line_of_tweet = raw_input("Invalid response.  Please enter a number corresponding to the tweet "
                                              "you'd like to view online: ")
                # Open the JSON file for reading and grab everything in there, then close the file
                with open('app/data/election.json', 'r') as data_file:
                    data = json.load(data_file)
                data_file.close()
                # Store the id string (id_str) of the desired tweet in the tweet_id variable
                tweet_id = data['Tweet' + line_of_tweet]['id_str']
                # Open a web browser and go to the URL for the tweet the user wanted to see displayed on the web
                browser = webbrowser.get("open -a /Applications/Google\ Chrome.app %s")
                browser.open('https://twitter.com/statuses/{0}'.format(tweet_id), new=1, autoraise=True)
            # Handle a NO response
            else:
                # Set 'loop' to be < 0 in order to stop the while loop handling the tweet viewing
                loop = -1
                print('')
                print('OK. Thanks for using this app. Come back soon and do another search!  Goodbye.')
