import os
from dotenv import load_dotenv


def read_credentials():
    """
    Return users os.getenv from the environnement variable
    raise a an exception if the os.getenv are empty
    
    Raises:
        NotImplementedError: (description]
    """
    load_dotenv()
    consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
    consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_secret = os.getenv('TWITTER_ACCESS_SECRET')

    if all([consumer_key, consumer_secret, access_token, access_secret]):
        return {"consumer_key": consumer_key, 
                "consumer_secret": consumer_key,
                "access_token": access_token,
                "access_secret": access_secret}
    else:
        raise ValueError('Please add a .env file and put the os.getenv on it,\
                         refer to the sample')
