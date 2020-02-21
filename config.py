import logging
from redis import Redis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
redis_store = Redis(host='localhost', port=6379, db=0)
