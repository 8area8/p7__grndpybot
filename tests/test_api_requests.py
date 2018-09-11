"""Pytest - api_requests.py."""

from unittest.mock import MagicMock

import pytest

from grandpybot.api_requests import request_google_place, MediaWiki


def fake_requests(json_value):
    """Create a fake requests mock with a fake json() value."""
    mock = MagicMock()
    mock.get().json.return_value = json_value
    return mock


def test_OK_status_google_place(monkeypatch):
    """Test if the function returns a dict with the needed values."""
    def json():
        """Return a fake json result from request."""
        location = {"lat": 20, "lng": 30}
        geometry = {"location": location}
        candidates = [{"formatted_address": "champ de Mars",
                       "geometry": geometry}]
        response = {"candidates": candidates, "status": "OK"}
        return response

    mock = fake_requests(json())
    monkeypatch.setattr("grandpybot.api_requests.requests", mock)

    response = request_google_place("tour eiffel")
    assert response["status"] == "OK"
    assert response["coords"] == {"lat": 20, "lng": 30}
    assert response["adress"] == "champ de Mars"


def test_NOT_status_google_place(monkeypatch):
    """Test if the function only return the status when the request fails."""
    json = {"status": "ZERO_RESULTS", "othersthinks": 187363}

    mock = fake_requests(json)
    monkeypatch.setattr("grandpybot.api_requests.requests", mock)

    response = request_google_place("zedrf")
    assert response["status"] == "ZERO_RESULTS"


def test_PROBLEM_status_google_place(monkeypatch):
    """Test if the function return a specific status when the request bugged.

    This occurs when requests encounters an error.
    """
    json = {}
    mock = fake_requests(json)
    monkeypatch.setattr("grandpybot.api_requests.requests", mock)

    response = request_google_place("tour eiffel")
    assert response["status"] == "PROBLEM_OCCURRED"


def test_OK_title_media_wiki(monkeypatch):
    """Test if the function returns a string title."""
    json = {"query": {"geosearch": [{"title": "Tour Eiffel"}]}}

    requests_mock = fake_requests(json)
    monkeypatch.setattr("grandpybot.api_requests.requests", requests_mock)
    monkeypatch.setattr("grandpybot.api_requests.choice", lambda list: list[0])

    response = MediaWiki.title_from_(20, 30)
    assert response == "Tour Eiffel"


def test_NOT_status_media_wiki(monkeypatch):
    """Test if the function return "None" when the request fail."""
    json = {"e": "z"}

    requests_mock = fake_requests(json)
    monkeypatch.setattr("grandpybot.api_requests.requests", requests_mock)

    response = MediaWiki.title_from_(20, 30)
    assert response is None


def test_OK_text_link_media_wiki(monkeypatch):
    """Test if the function returns a text and a link."""
    json = {"extract": "L'Hôtel Bourrienne est un hôtel.",
            "content_urls": {"desktop": {"page": "www.page.org"}}}

    requests_mock = fake_requests(json)
    monkeypatch.setattr("grandpybot.api_requests.requests", requests_mock)

    response = MediaWiki.text_and_link_from_("OpenClassroom")
    assert response[0] == "L'Hôtel Bourrienne est un hôtel."
    assert response[1] == "www.page.org"


def test_OK_coords_to_text_media_wiki(monkeypatch):
    """Test if the function return a dict with text and link."""
    def return_text_link(title):
        """Return a text and a link. Fake method."""
        return ("foo text", "www.bar.org")

    base_link = "grandpybot.api_requests.MediaWiki."
    monkeypatch.setattr(base_link + "title_from_", lambda lat, lng: "foo")
    monkeypatch.setattr(base_link + "text_and_link_from_", return_text_link)
    monkeypatch.setattr("grandpybot.api_requests.choice", lambda arg: "")

    response = MediaWiki.coords_to_text(20, 30)
    assert response["text"] == "foo text"
    assert response["wiki_link"] == "www.bar.org"


def test_NOT_coords_to_text_media_wiki(monkeypatch):
    """The function returns a specific text when the request fail."""
    base_link = "grandpybot.api_requests.MediaWiki."
    monkeypatch.setattr(base_link + "title_from_", lambda lat, lng: "")
    monkeypatch.setattr("grandpybot.api_requests.choice", lambda arg: "")

    response = MediaWiki.coords_to_text(20, 30)

    no_text = "Eh bien mon enfant, me voici en \"terra incognita\" !"
    wiki_link = "https://fr.wikipedia.org/wiki/Terra_incognita"
    assert response["text"] == no_text
    assert response["wiki_link"] == wiki_link


def test_NOT_TEXT_coords_to_text_media_wiki(monkeypatch):
    """The function a specific text when the request return an empty text."""
    def return_text_link(title):
        """Return a text and a link. Fake method."""
        return ("", "www.bar.org")

    base_link = "grandpybot.api_requests.MediaWiki."
    monkeypatch.setattr(base_link + "title_from_", lambda lat, lng: "foo")
    monkeypatch.setattr(base_link + "text_and_link_from_", return_text_link)
    monkeypatch.setattr("grandpybot.api_requests.choice", lambda arg: "")

    response = MediaWiki.coords_to_text(20, 30)

    no_text = "Mais les mots me manquent... Trop d'émotions."
    assert response["text"] == no_text
    assert response["wiki_link"] == "www.bar.org"
