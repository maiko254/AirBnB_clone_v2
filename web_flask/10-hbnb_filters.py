#!/usr/bin/python3
""" Starts a Flask web application """
from flask import Flask
from flask import render_template
from models import storage
from models.state import State
from models.amenity import Amenity

app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def hbnbfilters():
    """ """
    states = storage.all(State)
    amenities = storage.all(Amenity)
    return render_template("10-hbnb_filters.html", states=states, amenities=amenities)


@app.teardown_appcontext
def teardown_db(exception):
    """ Closes the current sql-alchemy session """
    if storage is not None:
        storage.close()


if __name__ == "__main__":
    """ Main function """
    app.run(host="0.0.0.0", port=5000)
