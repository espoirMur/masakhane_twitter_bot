from tweepy import Cursor, error as tweepy_error
from scripts.twitter_client import get_twitter_client
from joey_mnt_scripts.core import translate
from config import logger


class TwitterBot(object):
    def __init__(self, api, since_id, the_model):
        """
        This class create the twitter bot
        Args:
            object ([type]): [description]
            api ([type]): the twitter api
            since_id ([type]): the time since the last translation
            the_model ([type]): this should be a dictionary of loaded_model
        """
        self.api = api
        self.since_id = since_id
        self.the_model = the_model

    def check_mentions(self):
        """
        this is the bot itself it check the mention , get the text it was
        the mention was replying to and translate it
        Returns:
           new_since : the last time I tweeted
        """
        logger.info("Retrieving mentions")
        new_since_id = self.since_id
        for tweet in Cursor(self.api.mentions_timeline,
                            since_id=self.since_id).items():
            new_since_id = max(tweet.id, new_since_id)
            if tweet.in_reply_to_status_id:
                # only reply to a tweet if it's a reply to a tweet
                # TODOS: should get the language here
                parent_tweet = self.api.get_status(tweet.in_reply_to_status_id)
                # TODOS : check if the tweet is in english before translating
                # TODOS: More to be done on preprocesing with Tokenniser
                translated_tweet = ''.join([translate(sentence, **self.the_model)
                    for sentence in parent_tweet.text.split('.')])
                try:
                    self.api.update_status(status=translated_tweet,
                                           in_reply_to_status_id=tweet.id)
                except tweepy_error.TweepError as error:
                    if error.api_code == 187:
                        logger.error("You have already reply to this tweet")
                    else:
                        logger.error('an error occur')
                if not tweet.user.following:
                    try:
                        tweet.user.follow()
                    except tweepy_error.TweepError as error:
                        if error.api_code  == 158:
                            logger.error(f"I cannot follow my self")
                        else:
                            logger.error('an error occur')
            else:
                continue
        return new_since_id
