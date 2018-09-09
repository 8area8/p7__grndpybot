"""Request the APIs.

Each API function returns a dict.
"""

from random import choice

import requests

from grandpybot import app


def request_google_place(keywords):
    """Return a dict.

    The dict contains:
        . a request status
        . coordinates
        . a name
        . an adress
    """
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


def request_media_wiki(name):
    """Return a dict with a text and a link."""
    def random_introductions():
        """Return a random introduction text."""
        intros = ["Tiens tiens, je me souviens de ce lieu ! ",
                  "Aaaah ça y est, je vois ce que c'est ! ",
                  "Je suis déjà passé par là... ",
                  "J'ai des choses à t'apprendre. ",
                  "J'ai quelques souvenirs de cet endroit. "]
        return choice(intros)

    url = "https://fr.wikipedia.org/w/api.php"
    params = {"action": "opensearch", "search": name,
              "limit": "10", "namespace": "0", "format": "json"}

    req = requests.get(url, params=params).json()

    try:
        text = req[2][0]
        wiki_link = req[3][0]
    except IndexError:
        text = "Eh bien mon enfant, me voici en \"terra incognita\" !"
        wiki_link = "https://fr.wikipedia.org/wiki/Terra_incognita"
    else:
        if not text:
            text = "Mais les mots me manquent... L'émotion, sans doute."
        text = random_introductions() + text

    return {"text": text, "wiki_link": wiki_link}
