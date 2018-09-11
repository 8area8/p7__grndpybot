"""Flask init."""

import os
import json
from pathlib import Path

from flask import Flask


app = Flask(__name__)

is_production = os.environ.get('IS_HEROKU', None)
if is_production:
    app.config["GOOGLE_KEY"] = os.environ.get('GOOGLE_KEY')
else:
    app.config.from_object('flaskenv')

path_words = Path().resolve() / "grandpybot" / "stop_words.json"
with open(path_words, encoding='utf-8') as datas:
    stop_words = json.load(datas)


from grandpybot import views
