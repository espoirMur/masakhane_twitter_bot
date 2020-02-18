import os
import sys
from glob import glob
from dotenv import load_dotenv
from joey_mnt_scripts.core import load_model


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
                "consumer_secret": consumer_secret,
                "access_token": access_token,
                "access_secret": access_secret}
    else:
        raise ValueError('Please add a .env file and put the os.getenv on it,\
                         refer to the sample')


def load_models(path='transformer'):
    """
    Load all the models we have and return them as a dictionary of models
    Args:
        path (str, optional): path to the models in .
        Defaults to './transformer
    Return :
        models(dictionary): a dictionary where keys are models identifier
        and values are the values are the models.
    """
    the_models = dict()
    working_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    models_folder = os.path.join(working_dir, path)
    for folder in glob(f'{models_folder}/*/'):
        name = folder.split('/')[-2].replace('-', '_')
        the_models[name] = load_model(os.path.join(path, folder))
    return the_models
