from scripts.bot import TwitterBot
from scripts.twitter_client import get_twitter_client
from config import logger, redis_store
from time import sleep
from scripts.utils import load_models


if __name__ == "__main__":
    api = get_twitter_client()
    since_id = redis_store.get('since_id')
    if not since_id:
        since_id = 1
    else:
        since_id = int(since_id)
    the_models = load_models()
    while True:
        the_bot = TwitterBot(api, since_id, the_models)
        since_id = the_bot.check_mentions()
        redis_store.set('since_id', since_id)
        logger.info(f"Waiting...", )
        sleep(60)
