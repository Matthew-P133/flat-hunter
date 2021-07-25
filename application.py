from requests import NullHandler
from helpers import search
from helpers import convert_html_to_pdf
import helpers
from time import sleep, time
from datetime import datetime
from flask import Flask, render_template, request, redirect
import sqlite3
import json

# connect to db
db = sqlite3.connect("properties.db", check_same_thread=False)

app = Flask(__name__)

class Pdf():
    def render_pdf(self, name, html):
        from xhtml2pdf import pisa
    

        pdf = "testfile"
        pisa.CreatePDF(html, pdf)

        return pdf.getvalue()




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

    attributes = {
        "minBedrooms": 0,
        "maxBedrooms": 0,
        "floorplan": 1,
        "frequency": 0
    }
    
    if request.method == "GET":
        return redirect("/search")
    
    form_data = request.get_json()
    if form_data == None:
        form_data = request.form
    
    attributes["minBedrooms"] = form_data["minBedrooms"]
    attributes["maxBedrooms"] = form_data["maxBedrooms"]
    attributes["minPrice"] = form_data["minPrice"]
    attributes["maxPrice"] = form_data["maxPrice"]
    if "frequency" in form_data.keys():
        attributes["frequency"] = form_data["frequency"]

    if attributes["frequency"] == 0:
        # search once
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
    
    # TODO Schedule repeat search
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

    html = render_template("results.html", properties=properties, images=images)
    outputfile = f"FlatHunter-results-{datetime.now()}.pdf"
    convert_html_to_pdf(html, outputfile)
    return("Your results have been saved as a PDF (next feature to be implemented is emailing them to you!)")




@app.route("/email")

# TODO email the results in a pdf
def pdf():
    return("pdf")


