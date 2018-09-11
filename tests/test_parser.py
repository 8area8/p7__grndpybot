"""Pytest - parser.py."""

import pytest

from grandpybot.parser import Parser


@pytest.mark.parametrize("words", [
    ("bonjour"),
    ("Salut"),
    ("hey"),
    ("Hey papi tu peux me dire comment tu vas ?"),
    ("Yo le vieu, je veux ça"),
    (","),
    ("aujourd'hui")
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


@pytest.mark.parametrize("words", [
    ("veux,"),
    ("ok?"),
    ('non!')
])
def test_parser_remove_signs(words):
    """Test if the parser remove specifics signs."""
    assert Parser.parse(words) == ""


@pytest.mark.parametrize("words", [
    ("j'aimerai"),
    ("l'adresse"),
    ("n'aurais"),
    ("l'envie")
])
def test_parser_catch_apostrophs_early(words):
    """Test if the parser catch the french liaisons."""
    assert Parser.parse(words) == ""
