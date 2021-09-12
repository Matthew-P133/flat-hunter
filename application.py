from requests import NullHandler
from helpers import search
from helpers import convert_html_to_pdf
import helpers
from time import sleep, time
from datetime import datetime
from flask import Flask, render_template, request, redirect
import sqlite3
import json
import schedule
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from dotenv import dotenv_values

config = dotenv_values(".env")

# connect to db
db = sqlite3.connect("properties.db", check_same_thread=False)

app = Flask(__name__)


class Pdf():
    def render_pdf(self, name, html):
        from xhtml2pdf import pisa
        pdf = "testfile"
        pisa.CreatePDF(html, pdf)
        return pdf.getvalue()


def hunt(attributes):
    
    search(attributes)

    cursor = db.execute("SELECT MAX(search_id) FROM properties")
    max_search_id = cursor.fetchone()
    print(max_search_id[0])
    
    properties = []
    db.row_factory = sqlite3.Row
    cursor = db.execute("SELECT * FROM properties where search_id=?", [max_search_id[0]])
    
    for row in cursor:
        properties.append(row)

    images = []

    for property in properties:
        cursor = db.execute("SELECT * FROM images")
        for row in cursor:
            images.append(row)
    
    html = render_template("results.html", properties=properties, images=images)
    return html


def scheduled_hunt(attributes):

    search(attributes)

    cursor = db.execute("SELECT MAX(search_id) FROM properties")
    max_search_id = cursor.fetchone()
    print(max_search_id[0])
    
    properties = []
    db.row_factory = sqlite3.Row
    cursor = db.execute("SELECT * FROM properties where search_id=?", [max_search_id[0]])
    
    for row in cursor:
        properties.append(row)

    images = []

    for property in properties:
        cursor = db.execute("SELECT * FROM images")
        for row in cursor:
            images.append(row)
    
    html = render_template("results_for_email.html", properties=properties, images=images)
    
    outputfile = f"FlatHunter-results-{datetime.now()}.pdf"
    convert_html_to_pdf(html, outputfile)
    email_results(outputfile)


def email_results(outputfile):

    # configure details
    sender_address = config["address"]
    sender_pass = config["pass"]
    receiver_address = config["recipient"]

    # content
    mail_content = "Flats coming soon!"

    # Set up the email message
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Your latest FlatHunter results'

    # Configure attachment
    
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(f"{outputfile}", "rb").read())
    encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{outputfile}"')

    # put together email
    message.attach(MIMEText(mail_content, 'plain'))
    message.attach(part)

    #Create SMTP session and send the email
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass) 
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


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