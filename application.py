from helpers import scrape, url_generator
from time import sleep
from random import random
from flask import Flask

app = Flask(__name__)

@app.route("/")
# TODO homepage

@app.route("/search")

# TODO allow user to input preferences for attributes

@app.route("/results")

# TODO render results of search into html page(s)

@app.route("/email")

# TODO email the results in a pdf



"""# TO DO: dynamically pass in attributes
# attributes for testing
attributes = {
    "minBedrooms": 4,
    "maxBedrooms": 7,
    # "floorplan": 1,
}

# variable to count properties
i = 1

# generate URL based on attributes
url = url_generator(attributes)

# scrape page + update property counter
result = scrape(url, i)
i = result[1]

# add index of next page to attributes
page_dict = result[0]
index = page_dict["searchParameters"]["index"]
pagination = page_dict["pagination"]
attributes["index"] =  pagination["next"]

# until last page generate url of next page and scrape
while (int(pagination["next"]) <= int(pagination["last"])):
    url = url_generator(attributes)
    x = 10 * random()
    sleep(x)
    result = scrape(url, i)
    i = result[1]

    page_dict = result[0]
    pagination = page_dict["pagination"]
    if "next" not in pagination.keys():
        break
    attributes["index"] =  pagination["next"]"""
