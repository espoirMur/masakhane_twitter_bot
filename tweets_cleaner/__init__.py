import re
import unicodedata
import preprocessor as tweet_preprocessor
from .emoticons import emoticons
from nltk import tokenize


tweet_preprocessor.set_options(tweet_preprocessor.OPT.URL,
                               tweet_preprocessor.OPT.EMOJI,
                               tweet_preprocessor.OPT.RESERVED,
                               tweet_preprocessor.OPT.EMOJI,
                               tweet_preprocessor.OPT.SMILEY,
                               tweet_preprocessor.OPT.NUMBER,
                               tweet_preprocessor.OPT.MENTION)


class TweetsCleaner:

    def __init__(self):
        self.words_to_remove = emoticons
        self.emoji_patterns = re.compile("["
                                         u"\U0001F600-\U0001F64F"  # emoticons
                                         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                         u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                         # flags (iOS)
                                         u"\U0001F1E0-\U0001F1FF"
                                         u"\U00002702-\U000027B0"
                                         u"\U000024C2-\U0001F251"
                                         "]+", flags=re.UNICODE)

    def remove_nonlatin(self, s):
        """
        remove non ascii character but keep accent

        Args:
            s (string): text

        Returns:
            string: text without non ascii char
        """
        s = (ch for ch in s
             if unicodedata.name(ch).startswith(('LATIN', 'DIGIT', 'SPACE')))
        return ''.join(s)

    def remove_emoji(self, text):
        """
        remove the emojis and non ascii char with space from the tweet

        Args:
            text (string): text to clean

        Returns:
            string: cleaned text
        """
        # after tweepy preprocessing the colon symbol left remain after
        # removing mentions
        text = re.sub(r':', '', text)
        text = re.sub(r'‚Ä¶', '', text)
        # replace consecutive non-ASCII characters with a space
        text = ' '.join(
            re.findall(
                r'[\u0020-\u007F\u00A0-\u00FF\u0100-\u017F\u0180-\u024F]+',
                text))
        # remove emojis from tweet
        text = self.emoji_patterns.sub(r'', text)
        return text

    def pre_process_tweet(self, tweet):
        """
        Apply all the preprocessing process on a tweet and return
        the tweet as a text and tweet as list of tokens

        Args:
            tweet (object): tweet object to process

        Returns:
            list : list of sentences in the tweet
        """
        text = tweet_preprocessor.clean(tweet.text)
        text = text.replace('#', '')
        text = text.replace('-', '')
        text = text.replace("«", "")
        text = text.replace("»", "")
        text = text.replace("_", "")
        # handle sentences which end without space after point
        # check https://stackoverflow.com/a/44860184/4683950
        # check again if i should use sentences or the whole paragraph
        #text = re.sub(r'([a-z])\.([A-Z])', r'\1. \2', text)
        #sentences = tokenize.sent_tokenize(text)

        return text
