from helpers import search
from time import sleep
from random import random
from flask import Flask, render_template
import sqlite3

db = sqlite3.connect("properties.db", check_same_thread=False)

app = Flask(__name__)

@app.route("/")
# TODO homepage
def hompage():
    
    search()
    
    properties = []
    db.row_factory = sqlite3.Row
    cursor = db.execute("SELECT * FROM properties")
    for row in cursor:
              properties.append(row)

    images = []
    for property in properties:
        cursor = db.execute("SELECT * FROM images")
        for row in cursor:
            images.append(row)
    
    return render_template("results.html", properties=properties, images=images)


@app.route("/search")

# TODO allow user to input preferences for attributes
def preferences():
    return("preferences")

@app.route("/results")

# TODO render results of search into html page(s)
def results():
    return("results")

@app.route("/email")

# TODO email the results in a pdf
def pdf():
    return("pdf")
