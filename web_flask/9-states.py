#!/usr/bin/python3
""" Starts a Flask web application """
from flask import Flask
from flask import render_template
from models import storage
from models.state import State
from jinja2 import Environment
from jinja2.ext import loopcontrols

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config.from_object(__name__)


@app.route("/states")
@app.route("/states_list", strict_slashes=False)
def states_list():
    """ Renders a template with a list of all states in database """
    states = storage.all(State)
    return render_template("7-states_list.html", states=states)


@app.route("/cities_by_states", strict_slashes=False)
def cities_list():
    """
       Renders a template displaying a list of cities in a state in storage
    """
    states = storage.all(State)
    return render_template("8-cities_by_states.html", states=states)


@app.route("/states/<id>")
def states_id(id):
    """
       Displays a HTML page with the H1 tag State if id is found,
       H3 tag city and a list of City objects linked to the State
    """
    states = storage.all(State).values()
    found = 0
    state = ""
    for s in states:
        if id == s.id:
            found = 1
            state = s
            break
    return render_template("9-states.html", state=state, found=found)


@app.teardown_appcontext
def teardown_db(exception):
    """ Closes the current sql-alchemy session """
    if storage is not None:
        storage.close()


if __name__ == "__main__":
    """ Main function """
    app.run(host="0.0.0.0", port=5000)
