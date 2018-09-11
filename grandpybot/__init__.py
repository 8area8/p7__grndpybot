"""Flask init."""

import os
import json

from flask import Flask


app = Flask(__name__)

is_production = os.environ.get('IS_HEROKU', None)
if is_production:
    app.config["GOOGLE_KEY"] = os.environ.get('GOOGLE_KEY')
else:
    app.config.from_object('flaskenv')

with open("grandpybot.stop_words.json") as file:
    stop_words = json.load(file)

from grandpybot import views
