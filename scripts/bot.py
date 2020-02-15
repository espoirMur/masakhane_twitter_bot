from tweepy import Cursor, error as tweepy_error
from scripts.twitter_client import get_twitter_client
from joey_mnt_scripts.core import translate
from config import logger


def check_mentions(api, since_id, the_model):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id:
            # only reply to a tweet if it's a reply to a tweet
            parent_tweet = api.get_status(tweet.in_reply_to_status_id)
            # TODOS : check if the tweet is in english before translating
            translated_tweet = translate(parent_tweet.text, **the_model)
            try:
                api.update_status(status=translated_tweet,
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
