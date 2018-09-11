"""Parse the string input and return some key words."""

from grandpybot import stop_words


class Parser():
    """Parse the user input.

    Try to return a place.
    """
    @staticmethod
    def parse(sentence):
        """Parse a sentence."""
        sentence = sentence.lower().split()
        sentence = [word for word in sentence if word not in stop_words]
        sentence = " ".join(sentence)
        return sentence
