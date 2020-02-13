import os
import sys
import json
from tweepy import API
from tweepy import OAuthHandler
from utils import read_credentials


def get_twitter_auth():
    """Setup Twitter authentication.

    Return: tweepy.OAuthHandler object
    """
    try:
        credentials = read_credentials()
        consumer_key = credentials.get('consumer_key')
        consumer_secret = credentials.get('consumer_secret')
        access_token = credentials.get('access_token')
        access_secret = credentials.get('access_secret')
    except KeyError:
        sys.stderr.write("TWITTER_*  not found\n")
        sys.exit(1)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return auth


def get_twitter_client():
    """Setup Twitter API client.

    Return: tweepy.API object
    """
    auth = get_twitter_auth()
    client = API(auth)
    return client
