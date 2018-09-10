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


def request_media_wiki(coords):
    """Return a dict with a text and a link."""
    def random_introductions():
        """Return a random introduction text."""
        intros = ["Tiens tiens, je me souviens de ce lieu ! ",
                  "Aaaah ça y est, je vois ce que c'est ! ",
                  "Je suis déjà passé par là... ",
                  "J'ai des choses à t'apprendre. ",
                  "J'ai quelques souvenirs de cet endroit. "]
        return choice(intros)

    def find_page_id_from_coordinates(lat, lng):
        """Find the nearest place of coordinates."""
        url = "https://fr.wikipedia.org/w/api.php"
        params = {"action": "query", "list": "geosearch", "gsradius": "10000",
                  "gscoord": f"{lat}|{lng}", "format": "json"}
        req = requests.get(url, params=params).json()

        try:
            page_id = req["query"]["geosearch"]["pageid"]
        except KeyError:
            return None
        else:
            return page_id

    def find_text_from_id(page_id):
        """Find the explain text of the given page_id."""
        url = "https://fr.wikipedia.org/w/api.php"
        params = {"action": "query", "prop": "extracts", "exlimit": "max",
                  "explaintext": "", "exintro": "", "pageids": page_id,
                  "redirects": ""}
        req = requests.get(url, params=params).json()
        text = req["query"]["pages"][page_id]["extract"]
        return (text)

    lat, lng = coords
    page_id = find_page_id_from_coordinates(lat, lng)
    if not page_id:
        text = "Eh bien mon enfant, me voici en \"terra incognita\" !"
        wiki_link = "https://fr.wikipedia.org/wiki/Terra_incognita"
    else:
        text = find_text_from_id(page_id)
        if not text:
            text = "Mais les mots me manquent... Trop d'émotions."
        text = random_introductions() + text
        wiki_link = ("https://fr.wikipedia.org/w/"
                     f"index.php?title=AR-15&curid={page_id}")

    return {"text": text, "wiki_link": wiki_link}
