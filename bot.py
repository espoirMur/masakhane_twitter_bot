import tweepy
import logging
from twitter_client import get_twitter_client
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if not tweet.in_reply_to_status_id:
            continue
        logger.info(f"Answering to {tweet.user.name}")

        if not tweet.user.following:
            tweet.user.follow()

        api.update_status(status="Please reach us via DM",
                          in_reply_to_status_id=tweet.id)
    return new_since_id

def main():
    api = get_twitter_client()
    since_id = 1
    while True:
        since_id = check_mentions(api, ["help", "support"], since_id)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()
