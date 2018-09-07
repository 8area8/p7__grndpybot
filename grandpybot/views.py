"""Main file for views."""

from grandpybot import app
from flask import render_template, request


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
    req = request.args
    import pdb; pdb.set_trace()
    keywords = ""
    key = "AIzaSyDZrTwZdIVBsCMN0YbA4C5La7Ytb8OIWkw"
    url = ("https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
           f"input={keywords}&inputtype=textquery&fields=geometry&key={key}")
