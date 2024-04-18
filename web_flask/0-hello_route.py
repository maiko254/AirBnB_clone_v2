#!/usr/bin/python3
""" Starts a Flask web application listening on 0.0.0.0 and port 5000 """
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """ Defines a route that prints a message when / is requested """
    return "Hello HBNB!"


if __name__ == "__main__":
    """ Main function """
    app.run(host='0.0.0.0', port=5000)
