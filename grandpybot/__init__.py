"""Flask init."""

import os

from flask import Flask


app = Flask(__name__)

is_production = os.environ.get('IS_HEROKU', None)
if is_production:
    app.config["GOOGLE_KEY"] = os.environ.get('GOOGLE_KEY')
else:
    app.config.from_object('flaskenv')

from grandpybot import views
