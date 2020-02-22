from tweepy import Cursor, error as tweepy_error
from joey_mnt_scripts.core import translate
from tweets_cleaner import TweetsCleaner
from config import logger


class TwitterBot(object):
    def __init__(self, api, since_id, the_models):
        """
        This class create the twitter bot
        Args:
            object ([type]): [description]
            api ([type]): the twitter api
            since_id ([type]): the time since the last translation
            the_models ([type]): this should be a dictionary of loaded_models
        """
        self.api = api
        self.since_id = since_id
        self.the_models = the_models
        self.tweet_cleaner = TweetsCleaner()

    def translate_text(self, sentence, model):
        """
        Given the model and the text translate the text and return the
        translated text

        Args:
            text ([type]): Array of sentences to transalate
            model ([type]): the model to use to translate
        """
        # translated_text = '. '.join(
        #    [translate(sentence, **model) for sentence in text])
        return '. '.join([translate(text, **model) for text in sentence])

    def reply_to_tweet(self, reply_message, tweet_id):
        """
        Reply to a tweet with the id passed in parameter with the message
        Args:
            reply_message (string): the message to reply to the user
            tweet_id (int): tweet id
        """
        try:
            self.api.update_status(status=reply_message,
                                   in_reply_to_status_id=tweet_id)
        except tweepy_error.TweepError as error:
            if error.api_code == 187:
                logger.error("You have already reply to this tweet")
            else:
                logger.error('an error occur')

    def check_parent_tweet_language(self, tweet, language_check):
        """
        Check tweet language
        Args:
            array_list of languages
            tweet ([type]): tweet
        """
        language = tweet.lang
        if language not in language_check:
            message = 'this language is not supported yet'
            self.reply_to_tweet(message, tweet.id)
            return False
        else:
            return language

    def get_target_language(self, tweet):
        """
        Return tweet target langauges

        Args:
            tweet (string): the tweet
        """
        # TODO : this can be refactored
        if 'swc' in tweet.text or 'ln' in tweet.text:
            if 'swc' in tweet.text:
                return "swc"
            elif 'ln' in tweet.text:
                return 'ln'
        else:
            message = "The target language is not specified"\
                " or not supported yet add ln or swc in mention"
            self.reply_to_tweet(message, tweet.id)
            return False

    def follow_back_user(self, user):
        """
        Follow back the user who tweeted

        Args:
            user (object): twitter user
        """
        if not user.following:
            try:
                user.follow()
            except tweepy_error.TweepError as error:
                if error.api_code == 158:
                    logger.error(f"I cannot follow my self")
                else:
                    logger.error('an error occur')

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
            logger.info(
                f"{self.since_id} Okay what is happening? {new_since_id}")
            if tweet.in_reply_to_status_id:
                # if the tweet is in the format mention space target_lan_code
                # only reply to a tweet if it's a reply to a tweet
                target_language = self.get_target_language(tweet)
                parent_tweet = self.api.get_status(tweet.in_reply_to_status_id)
                source_language = self.check_parent_tweet_language(
                    parent_tweet, ['en', 'fr'])
                if source_language and target_language:
                    language_model = f'{source_language}_{target_language}'
                    model = self.the_models.get(language_model)
                    if model:
                        tweet_cleaned = self.tweet_cleaner.pre_process_tweet(
                            parent_tweet)
                        # need to check this
                        translated_tweet = self.translate_text(tweet_cleaned,
                                                               model)
                        self.reply_to_tweet(translated_tweet, tweet.id)
                        self.follow_back_user(tweet.user)
                        logger.info(
                            f"we got this {tweet_cleaned}"
                            "and replied with this {translated_tweet}")
                else:
                    continue
            else:
                continue
        return new_since_id
