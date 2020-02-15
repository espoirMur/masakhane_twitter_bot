from scripts.bot import check_mentions
from scripts.twitter_client import get_twitter_client
from config import logger
from time import sleep
from joey_mnt_scripts.core import translate, load_model


if __name__ == "__main__":
    api = get_twitter_client()
    since_id = 1
    the_model = load_model("./transformer")
    while True:
        since_id = check_mentions(api, since_id, the_model)
        logger.info(f"Waiting...", )
        sleep(60)
