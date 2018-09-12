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
        lowered = sentence.lower()
        removed_signs = re.sub('[!@#$?,:;.]', '', lowered)
        removed_apostrophes = re.sub(r'(\s|^)\w{1}\'', ' ', removed_signs)

        keywords = removed_apostrophes.split()
        filtered = [word for word in keywords if word not in stop_words]

        return " ".join(filtered)
