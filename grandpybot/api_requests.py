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
              "fields": "formatted_address,geometry,name",
              "language": "fr", "key": key}

    req = requests.get(url, params=params).json()
    try:
        response = {"status": req["status"]}
        if response["status"] == "OK":
            response["coords"] = req["candidates"][0]["geometry"]["location"]
            response["adress"] = req["candidates"][0]["formatted_address"]
            response["name"] = req["candidates"][0]["name"]
    except (KeyError, IndexError):
        response = {"status": "PROBLEM_OCCURRED"}

    return response


def request_media_wiki(coords, name):
    """Return a dict with two texts and a link."""
    return MediaWiki.coords_to_text(coords["lat"], coords["lng"], name)


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
    def place_text_from_(cls, title):
        """Return the classical description of the needed place."""
        url = "https://fr.wikipedia.org/w/api.php"
        params = {"action": "query", "list": "search", "srsearch": title, "utf8": "", "format": "json"}
        req = requests.get(url, params=params).json()

        try:
            title_for_extract = req["query"]["search"][0]["title"].replace(" ", "_")

            url = f"https://fr.wikipedia.org/api/rest_v1/page/summary/{title_for_extract}"
            req = requests.get(url).json()
            base_text = "Laisse moi regarder dans le dictionnaire... "
            text = base_text + req["extract"]
        except (KeyError, IndexError):
            text = "Mon dictionnaire ne renvoie rien sur ce lieu..."

        return text


    @classmethod
    def coords_to_text(cls, lat, lng, name):
        """Get the two texts and the link from coordinates."""
        title = cls.title_from_(lat, lng)
        place_text = cls.place_text_from_(name)

        if not title:
            anecdote = "Eh bien mon enfant, me voici en \"terra incognita\" !"
            wiki_link = "https://fr.wikipedia.org/wiki/Terra_incognita"

        else:
            anecdote, wiki_link = cls.text_and_link_from_(title)

            if not anecdote:
                anecdote = "Mais les mots me manquent... Trop d'émotions."
            anecdote = choice(cls.intros) + anecdote

        return {"place_text": place_text, "anecdote": anecdote, "wiki_link": wiki_link}
