"""Main file for views."""

from grandpybot import app, render_template


@app.route('/')
@app.route('/index/')
def hello_world():
    """Return the main file."""
    return render_template('index.html')


@app.errorhandler(404)
def not_found(error):
    """If 404 error."""
    return (render_template('404.html'), 404)
