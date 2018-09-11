"""Pytest - parser.py."""

import pytest

from grandpybot.parser import Parser


@pytest.mark.parametrize("words", [
    ("bonjour"),
    ("Salut"),
    ("hey"),
    ("Hey papi tu peux me dire comment tu vas ?")
])
def test_parser_catch_(words):
    """Test if the parser catch the givens words."""
    assert Parser.parse(words) == ""


@pytest.mark.parametrize("words", [
    ("Paris"),
    ("Lac"),
    ("Irlande")
])
def test_parser_return_lower(words):
    """Test if the parser return the lowers words."""
    assert Parser.parse(words) == words.lower()
