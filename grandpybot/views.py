"""Main file for views."""

from flask import render_template, request

from grandpybot import app
from grandpybot.api_requests import req_google_place, req_media_wiki


@app.route('/index/')
@app.route('/')
def index():
    """Return the main file."""
    key = app.config["GOOGLE_KEY"]
    url = ("https://maps.googleapis.com/maps/"
           f"api/js?key={key}&callback=initMap")

    return render_template('index.html', url_map_api=url, title="home")


@app.errorhandler(404)
def not_found(error):
    """If 404 error."""
    return (render_template('404.html'), 404)


@app.route('/about/')
def about():
    """Return the about file."""
    return render_template('about.html', title="qui suis-je ?")


@app.route('/google_place_request', methods=['GET', 'POST'])
def place_request():
    """Send a request to the Google place API.

    Return the response.
    """
    req = req_google_place(request.form["data"])

    name = req.json()["candidates"][0]["name"]
    text_info = req_media_wiki(name)

    return req.text


@app.after_request
def add_header(req):
    """Add headers to both force latest IE rendering engine or Chrome Frame.

    Also to cache the rendered page for 10 minutes.
    """
    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
