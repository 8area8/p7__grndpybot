"""Request the APIs."""

import requests

from grandpybot import app


def req_google_place(keywords):
    """Return the name and coordinates."""
    key = app.config["GOOGLE_KEY"]
    url = ("https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
           f"input={keywords}&inputtype=textquery&fields=geometry,name"
           f"&language=fr&key={key}")

    req = requests.get(url).json()
    status = req["status"]
    coords = req["candidates"][0]["geometry"]["location"]
    name = req["candidates"][0]["name"]
    return {"status": status, "coords": coords, "name": name}


def req_media_wiki(name):
    """Return a response with an article."""
    url = ("https://fr.wikipedia.org/w/api.php?action=opensearch"
           f"&search={name}&limit=10&namespace=0&format=json")

    req = requests.get(url).json()
    text = req[2][0]
    return text
