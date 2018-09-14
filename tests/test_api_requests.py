"""Pytest - api_requests.py."""

from unittest.mock import MagicMock

from grandpybot.api_requests import request_google_place, MediaWiki


def fake_requests(*args):
    """Create a fake requests mock with a fake json() value."""
    mock = MagicMock()
    mock.get().json.side_effect = args
    return mock


def test_OK_status_google_place(monkeypatch):
    """Test if the function returns a dict with the needed values."""
    def json():
        """Return a fake json result from request."""
        location = {"lat": 20, "lng": 30}
        geometry = {"location": location}
        candidates = [{"formatted_address": "champ de Mars",
                       "geometry": geometry,
                       "name": "Tour Eiffel"}]
        response = {"candidates": candidates, "status": "OK"}
        return response

    mock = fake_requests(json())
    monkeypatch.setattr("grandpybot.api_requests.requests", mock)

    response = request_google_place("tour eiffel")
    assert response["status"] == "OK"
    assert response["coords"] == {"lat": 20, "lng": 30}
    assert response["adress"] == "champ de Mars"
    assert response["name"] == "Tour Eiffel"


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
    json = {"query": {"geosearch": [{"title": "Tour Eiffel", "foo": {"foo": "bar"}}]}}

    requests_mock = fake_requests(json)
    monkeypatch.setattr("grandpybot.api_requests.requests", requests_mock)
    monkeypatch.setattr("grandpybot.api_requests.choice", lambda list: list[0])

    response = MediaWiki.title_from_(20, 30, "")
    assert response == "Tour Eiffel"


def test_NOT_status_media_wiki(monkeypatch):
    """Test if the function return "None" when the request fail."""
    json = {"e": "z"}

    requests_mock = fake_requests(json)
    monkeypatch.setattr("grandpybot.api_requests.requests", requests_mock)

    response = MediaWiki.title_from_(20, 30, "")
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
    monkeypatch.setattr(base_link + "title_from_", lambda lat, lng, place: "foo")
    monkeypatch.setattr(base_link + "text_and_link_from_", return_text_link)
    monkeypatch.setattr("grandpybot.api_requests.choice", lambda text: "")

    response = MediaWiki.coords_to_text(20, 30, "te")
    assert response["anecdote"] == "foo text"
    assert response["wiki_link"] == "www.bar.org"


def test_NOT_coords_to_text_media_wiki(monkeypatch):
    """The function returns a specific text when the request fail."""
    base_link = "grandpybot.api_requests.MediaWiki."
    monkeypatch.setattr(base_link + "title_from_", lambda lat, lng, place: "")
    monkeypatch.setattr("grandpybot.api_requests.choice", lambda text: "")

    response = MediaWiki.coords_to_text(20, 30, "te")

    no_text = "Eh bien mon enfant, me voici en \"terra incognita\" !"
    wiki_link = "https://fr.wikipedia.org/wiki/Terra_incognita"
    assert response["anecdote"] == no_text
    assert response["wiki_link"] == wiki_link


def test_NOT_TEXT_coords_to_text_media_wiki(monkeypatch):
    """The function a specific text when the request returns an empty text."""
    def return_text_link(title):
        """Return a text and a link. Fake method."""
        return ("", "www.bar.org")

    base_link = "grandpybot.api_requests.MediaWiki."
    monkeypatch.setattr(base_link + "title_from_", lambda lat, lng, place: "foo")
    monkeypatch.setattr(base_link + "text_and_link_from_", return_text_link)
    monkeypatch.setattr("grandpybot.api_requests.choice", lambda arg: "")

    response = MediaWiki.coords_to_text(20, 30, "Tour_Eiffel")

    no_text = "Mais les mots me manquent... Trop d'émotions."
    assert response["anecdote"] == no_text
    assert response["wiki_link"] == "www.bar.org"


def test_OK_place_text_media_wiki(monkeypatch):
    """The function returns the place needed text."""
    json_title = {"query": {"search": [{"title": "Tour Eiffel"}]}}
    json_extract = {"extract": "la tour eiffel."}
    mocks = fake_requests(json_title, json_extract)

    monkeypatch.setattr("grandpybot.api_requests.requests", mocks)
    place_text = MediaWiki.place_text_from_("tour eiffel")
    base_text = "Laisse moi regarder dans le dictionnaire... "
    assert place_text == (base_text + "la tour eiffel.", "Tour Eiffel")

def test_NOT__place_text_media_wiki(monkeypatch):
    """Function returns a specific text when the request fail."""
    json_title = {"query": {"search": [{"title": "Tour Eiffel"}]}}
    json_extract = {}
    mocks = fake_requests(json_title, json_extract)

    monkeypatch.setattr("grandpybot.api_requests.requests", mocks)
    place_text = MediaWiki.place_text_from_("tour eiffel")
    assert place_text == ("Mon dictionnaire ne renvoie rien sur ce lieu...", "Tour Eiffel")
