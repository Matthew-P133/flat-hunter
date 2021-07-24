from helpers import search
from helpers import convert_html_to_pdf
import helpers
from time import sleep
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

# TODO allow user to input preferences for attributes
def preferences():
    return render_template("search.html")


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
    }
    
    if request.method == "GET":
        return redirect("/search")
    
    form_data = request.get_json()
    
    attributes["minBedrooms"] = form_data["minBedrooms"]
    attributes["maxBedrooms"] = form_data["maxBedrooms"]
    attributes["minPrice"] = form_data["minPrice"]
    attributes["maxPrice"] = form_data["maxPrice"]

    print(f"{attributes}")
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
    #html = "<body>Hello</body>"
    print(html)

    outputfile = "outputfile.pdf"

    convert_html_to_pdf(html, outputfile)

    return html




@app.route("/email")

# TODO email the results in a pdf
def pdf():
    return("pdf")
