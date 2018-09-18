"""Pytest package."""

from unittest.mock import MagicMock


def fake_requests(*args):
    """Create a fake requests mock with a fake json() value."""
    mock = MagicMock()
    mock.get().json.side_effect = args
    return mock
