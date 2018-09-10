"""Pytest - api_requests.py."""

from unittest.mock import MagicMock
import pytest

from grandpybot.api_requests import request_google_place, request_media_wiki
import grandpybot.api_requests as api



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
    assert len(response.keys()) == 1
