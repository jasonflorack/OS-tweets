from tweepy import OAuthHandler

# Developers: enter your own keys and secrets here to enable the app to run!
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''


def return_auth():
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return auth