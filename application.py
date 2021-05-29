from helpers import search
from time import sleep
from random import random
from flask import Flask, render_template, request, redirect
import sqlite3

db = sqlite3.connect("properties.db", check_same_thread=False)

app = Flask(__name__)

@app.route("/")
# TODO homepage
def hompage():
    return render_template("index.html")
    

@app.route("/search")

# TODO allow user to input preferences for attributes
def preferences():
    return render_template("search.html")

@app.route("/results", methods=['GET', 'POST'])

# TODO render results of search into html page(s)
def results():

    attributes = {
        "minBedrooms": 0,
        "maxBedrooms": 0,
        "floorplan": 1,
    }
    
    if request.method == "GET":
        return redirect("/search")
    
    attributes["minBedrooms"] = request.form.get("minBedrooms")
    attributes["maxBedrooms"] = request.form.get("maxBedrooms")
    attributes["minPrice"] = request.form.get("minPrice")
    attributes["maxPrice"] = request.form.get("maxPrice")

    search(attributes)
    
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


@app.route("/email")

# TODO email the results in a pdf
def pdf():
    return("pdf")
