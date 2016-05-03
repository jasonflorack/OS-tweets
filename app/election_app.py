import os
import sys
sys.path.insert(0, os.path.abspath(".."))
from app.UserInterface import UserInterface
from config import return_auth


class ElectionApp:

    @staticmethod
    def run_app():
        u = UserInterface()
        auth = return_auth()
        u.auth = auth
        u.clear_screen()
        u.greeting()
        u.pick_recent_or_live_tweets()
        u.view_tweet_in_browser_or_end_program()


