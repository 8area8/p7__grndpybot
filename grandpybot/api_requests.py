"""Request the APIs."""

import requests

from grandpybot import app


def req_google_place(keywords):
    """Return the name and coordinates."""
    key = app.config["GOOGLE_KEY"]
    url = ("https://maps.googleapis.com/maps/api/place/findplacefromtext/json")
    params = {"input": keywords, "inputtype": "textquery",
              "fields": "formatted_address,geometry,name",
              "language": "fr", "key": key}

    req = requests.get(url, params=params).json()
    status = req["status"]
    coords = req["candidates"][0]["geometry"]["location"]
    name = req["candidates"][0]["name"]
    adress = req["candidates"][0]["formatted_address"]
    return {"status": status, "coords": coords, "name": name, "adress": adress}


def req_media_wiki(name):
    """Return a response with an article."""
    url = ("https://fr.wikipedia.org/w/api.php?action=opensearch"
           f"&search={name}&limit=10&namespace=0&format=json")

    req = requests.get(url).json()
    intro = "Tiens tiens, je me souviens de ce lieu ! "
    text = intro + req[2][0]
    wiki_link = req[3][0]
    return text, wiki_link
