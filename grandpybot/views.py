"""Main file for views."""

from flask import render_template, request, jsonify

from grandpybot import app
from grandpybot.api_requests import request_google_place, request_media_wiki
from grandpybot.parser import Parser


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


@app.route('/api_request', methods=['GET', 'POST'])
def place_request():
    """Send request to Google place API and Media Wiki API.

    Return the response.
    """
    user_input = request.form["data"]
    parsed_input = Parser.parse(user_input)

    response = request_google_place(parsed_input)
    if response["status"] == "OK":
        response.update(request_media_wiki(response["coords"]))

    return jsonify(response)


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
