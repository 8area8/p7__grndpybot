"""Pytest - api_requests.py."""

from grandpybot.api_requests import request_google_place, MediaWiki
from tests import fake_requests


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
