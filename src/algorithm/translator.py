from googletrans import Translator as GoogleTranslator


class Translator:
    """Translator wrapper. """

    _translator = None
    """Translator instance. """

    def __init__(self):
        self._translator = GoogleTranslator()

    def to_english(self, text: str) -> str:
        """Returns strings translated to English.

        :param text:
        :return:
        """
        translation = self._translator.translate(text, src='es', dest='en')

        return translation.text
