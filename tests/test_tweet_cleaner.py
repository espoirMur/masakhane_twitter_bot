from unittest import TestCase
from unittest.mock import Mock
from tweets_cleaner import TweetsCleaner


class TestTwitterCleaner(TestCase):
    tweet_cleaner = TweetsCleaner()
    source_sentence = "This episode of Love Island really"\
        " puts me off ever having another child."\
        "The noises they make. Crying every day."\
        "The way they laze around the pool all day hoping to become famous."\
        "I just can’t face it."
    tweet = Mock()
    tweet.__setattr__("text", source_sentence)

    def test_can_clean_tweet(self):
        cleaned_tweet = self.tweet_cleaner.pre_process_tweet(tweet=self.tweet)
        self.assertEquals(
            cleaned_tweet,
            "This episode of Love Island really puts me off ever having another child."\
            "The noises they make. Crying every day."\
            "The way they laze around the pool all day hoping to become famous."\
            "I just can’t face it.")

        another_source = "Today was the first day when I realized I was experiencing burnout."\
                        "After two major incidents and dramatically increased scrutiny, "\
                        "I'm really starting to feel it."
        self.tweet.__setattr__('text', another_source)
        another_source_cleaned = self.tweet_cleaner.pre_process_tweet(self.tweet)
        self.assertEquals(another_source_cleaned, "Today was the first day when"\
                                                    " I realized I was eeriencing burnout."\
                                                    "After two major incidents and dramatically"\
                                                    " increased scrutiny, I'm really starting to feel it.")
