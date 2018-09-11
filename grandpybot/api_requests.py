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
        . an adress
    If the request fail, the dict only contains the status.

    TODO: Create a log file when an exception occurs.
    """
    key = app.config["GOOGLE_KEY"]
    url = ("https://maps.googleapis.com/maps/api/place/findplacefromtext/json")
    params = {"input": keywords, "inputtype": "textquery",
              "fields": "formatted_address,geometry",
              "language": "fr", "key": key}

    req = requests.get(url, params=params).json()
    try:
        response = {"status": req["status"]}
        if response["status"] == "OK":
            response["coords"] = req["candidates"][0]["geometry"]["location"]
            response["adress"] = req["candidates"][0]["formatted_address"]
    except (KeyError, IndexError):
        response = {"status": "PROBLEM_OCCURRED"}

    return response


def request_media_wiki(coords):
    """Return a dict with a text and a link."""
    return MediaWiki.coords_to_text(coords["lat"], coords["lng"])


class MediaWiki():
    """MediaWiki class."""

    intros = ["Tiens, ça me rappel un endroit ! ",
              "Ah pas très loin d'ici, papi a vécu des choses ! ",
              "Je connais un peu les alentours ! ",
              "Papi a une histoire sur les environs ! ",
              "Papi a quelques souvenirs de ce quartier. ;) "]

    @classmethod
    def title_from_(cls, lat, lng):
        """Find the nearest place of coordinates.

        Return the place title.
        """
        url = "https://fr.wikipedia.org/w/api.php"
        params = {"action": "query", "list": "geosearch", "gsradius": "10000",
                  "gscoord": f"{lat}|{lng}", "format": "json"}
        req = requests.get(url, params=params).json()

        try:
            title = choice(req["query"]["geosearch"])["title"]
        except (KeyError, IndexError):
            return None
        else:
            return title

    @classmethod
    def text_and_link_from_(cls, title):
        """Find the explain text of the given title.

        Return the explain text and the wikipedia link.
        """
        url = f"https://fr.wikipedia.org/api/rest_v1/page/summary/{title}"
        req = requests.get(url).json()
        text = req["extract"]
        wiki_link = req["content_urls"]["desktop"]["page"]
        return (text, wiki_link)

    @classmethod
    def coords_to_text(cls, lat, lng):
        """Get the text and the link from coordinates."""
        title = cls.title_from_(lat, lng)

        if not title:
            text = "Eh bien mon enfant, me voici en \"terra incognita\" !"
            wiki_link = "https://fr.wikipedia.org/wiki/Terra_incognita"
        else:
            text, wiki_link = cls.text_and_link_from_(title)

            if not text:
                text = "Mais les mots me manquent... Trop d'émotions."
            text = choice(cls.intros) + text

        return {"text": text, "wiki_link": wiki_link}
