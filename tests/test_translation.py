from unittest import TestCase, skip
from unittest.mock import Mock
from scripts.utils import load_models
from scripts.bot import TwitterBot


class TranslationText(TestCase):
    source_sentence = "This episode of Love Island really"\
        " puts me off ever having another child."\
        "The noises they make. Crying every day."\
        "The way they laze around the pool all day hoping to become famous."\
        "I just can’t face it."
    the_models = load_models()
    the_bot = TwitterBot(Mock(), 1, the_models)  # to be changed

    def test_transalate(self):

        translated_text = self.the_bot.translate_text(
            self.source_sentence,
            self.the_models.get('en_ln'))
        self.assertEqual(
            "Likambo wana ya nsɔ́mɔ epusaki ngai mpenza na kozala na ezalela"
            " mosusu ya mpasi oyo bazalaki na yango na boumeli "
            "ya mokolo mobimba mpo na kokóma na elongi .", translated_text)
