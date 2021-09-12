from requests import NullHandler
from helpers import search
from helpers import hunt
from helpers import scheduled_hunt
import helpers
from time import sleep, time
from flask import Flask, render_template, request, redirect
import sqlite3
import json
import schedule


app = Flask(__name__)


@app.route("/")

# TODO homepage
def hompage():
    return render_template("index.html")
    

@app.route("/search")

def preferences():
    return render_template("search.html")


@app.route("/schedule")

def scheduler():
    return render_template("schedule.html")


@app.route("/loading", methods=['GET', 'POST'])

def loading():
    return render_template("loading.html", form_data=json.dumps(request.form))


@app.route("/status")

def status():
    status = {"last": str(helpers.last), "counter": str(helpers.counter)}
    return render_template("status.html", status=status)

@app.route("/results", methods=['GET', 'POST'])

def results():
    # default attributes
    attributes = {
        "minBedrooms": 0,
        "maxBedrooms": 0,
        "floorplan": 1,
        "frequency": 0
    }
    
    if request.method == "GET":
        return redirect("/search")
    
    #populate attributes dictionary with user input
    form_data = request.get_json()
    if form_data == None:
        form_data = request.form
    
    attributes["minBedrooms"] = form_data["minBedrooms"]
    attributes["maxBedrooms"] = form_data["maxBedrooms"]
    attributes["minPrice"] = form_data["minPrice"]
    attributes["maxPrice"] = form_data["maxPrice"]
    if "frequency" in form_data.keys():
        attributes["frequency"] = form_data["frequency"]
    
    # if 'search now' return webpage
    if attributes["frequency"] == 0:
        return hunt(attributes)
    
    # if 'schedule a search' generate pdf and schedule further searches
    if attributes["frequency"] == "Hourly":
        delay = 60
    elif attributes["frequency"] == "Daily":
        delay = 1440
    elif attributes["frequency"] == "Weekly":
        delay = 10080

    schedule.every(delay).minutes.do(scheduled_hunt, attributes)

    while 1:
        schedule.run_pending()
        sleep(1)