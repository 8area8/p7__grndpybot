"""Main file for views."""

from flask import render_template, request
import requests

from grandpybot import app


@app.route('/')
@app.route('/index/')
def index():
    """Return the main file."""
    return render_template('index.html')


@app.errorhandler(404)
def not_found(error):
    """If 404 error."""
    return (render_template('404.html'), 404)



@app.route('/about/')
def about():
    """Return the about file."""
    return render_template('about.html')


@app.route('/google_place_request', methods=['GET', 'POST'])
def place_request():
    """Send a request to the Google place API."""
    keywords = request.form["data"]
    key = app.config["GOOGLE_KEY"]
    url = ("https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
           f"input={keywords}&inputtype=textquery&fields=geometry&key={key}")
    req = requests.get(url)
    print(req.text)
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
