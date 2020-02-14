from tweepy import Cursor, error as tweepy_error
import logging
from twitter_client import get_twitter_client
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id:
            # only reply to a tweet if it's a reply to a tweet
            parent_tweet = api.get_status(tweet.in_reply_to_status_id)
            logger.info(parent_tweet.text, "=======>", 'we are translating this')
            logger.info(f"Answering to {tweet.user.name}")
            
            try:
                api.update_status(status="We are working on your tweet of your",
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


def main():
    api = get_twitter_client()
    since_id = 1
    while True:
        since_id = check_mentions(api, ["help", "support"], since_id)
        logger.info(f"Waiting...{since_id}", )
        time.sleep(60)

if __name__ == "__main__":
    main()
