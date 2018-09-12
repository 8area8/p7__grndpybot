"""Parse the string input and return some key words."""

import re

from grandpybot import stop_words


class Parser():
    """Parse the user input.

    Try to return a string place/adresse.
    """

    @staticmethod
    def parse(sentence):
        """Parse a sentence."""
        sentence = re.sub('[!@#$?,:;.]', '', sentence)
        sentence = re.sub(r'(\s|^)\w{1}\'', ' ', sentence)

        keywords = sentence.lower().split()
        filtered = [word for word in keywords if word not in stop_words]

        return " ".join(filtered)
