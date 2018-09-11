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
    ("aujourd'hui"),
    ("idée"),
    ("situé"),
    ("avoir"),
    ("coucou papi, t'aurais pas ?")
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


@pytest.mark.parametrize("words,excpected", [
    ("Salut papi, j'aimerai avoir l'adresse de sète stp.", "sète"),
    ("coucou grand père, t'aurais pas une idée d'où" +
     " est situé Paris par hasard?", "paris"),
    ("yo papi, j'veux bien l'adresse du groenland si ça t'chante!",
     "groenland"),
    ("hey, tu n'aurais pas un idée d'où se situe la rue des" +
     " rosiers par hasard?", ("rue rosiers"))
])
def test_parser_test_completes_sentences(words, excpected):
    """Situationals tests."""
    assert Parser.parse(words) == excpected
