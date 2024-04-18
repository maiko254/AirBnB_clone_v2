#!/usr/bin/python3
""" Starts a Flask web application listening on 0.0.0.0 and port 5000 """
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """ Defines a route that prints a message when / is requested """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """ Prints HBNB when /hbnb route is requested """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def cisfun(text):
    """ Prints C followed by value of the text variable """
    formatted_text = text.replace("_", " ")
    return f"C {formatted_text}"


@app.route("/python/", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def pythonisfun(text="is cool"):
    """ Prints Python followed by value of the text variable """
    formatted_text = text.replace("_", " ")
    return f"Python {formatted_text}"


if __name__ == "__main__":
    """ Main function """
    app.run(host='0.0.0.0', port=5000)
