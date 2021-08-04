import requests
from bs4 import BeautifulSoup
import json
import sqlite3
from PIL import Image
import os
from time import sleep
from random import random
from xhtml2pdf import pisa
 
# initialise counter variables
i = 1
counter = 0
last = "[calculating]"


def search(attributes): 
    #ensure variables have default values
    global i
    global counter
    global last
    i = 1
    counter = 0
    last = "[calculating]"

    db = sqlite3.connect("properties.db")

    # set search id
    cursor = db.execute("SELECT MAX(search_id) FROM properties")
    search_id = cursor.fetchone()
    if search_id[0] == None:
        new_search_id = 1
    else:
        new_search_id = search_id[0] + 1

    # generate URL based on attributes
    url = url_generator(attributes)

    # scrape page
    result = scrape(url, i, new_search_id)
    page_data = result[0]

    #update counter
    i = result[1]

    # access pagination details
    index = page_data["searchParameters"]["index"]
    pagination = page_data["pagination"]

    # generate number of properties (for loading screen)
    last = "approx. " + str(int(pagination["last"]) + 24)

    # quit if error (avoid looping over same page)
    if "next" not in pagination.keys():
            return 1
    
    # update attributes for next page to scrape 
    attributes["index"] = pagination["next"]

    # until last page generate url of next page and scrape
    while (int(pagination["next"]) <= int(pagination["last"])):
        url = url_generator(attributes)

        # random wait between scrapes
        wait = 10 * random()
        sleep(wait)

        #scrape page
        result = scrape(url, i, new_search_id)
        page_data = result[0]
        i = result[1]

        # increment target for scraping
        pagination = page_data["pagination"]
        if "next" not in pagination.keys():
            return 1
        attributes["index"] = pagination["next"]
    


def scrape(url, i, new_search_id):
    # get page html and write to file
    page = requests.get(url)
    # if page.status_code != 200:
        # TODO return error
    f = open("page.html", "w")
    f.write(f"{page.text}")
    f.close()

    # parse html
    with open("page.html") as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    # find element containing property data and write to file
    x = soup.find_all("script")
    for tag in x:
        a = str(tag.string)
        if "window.jsonModel = {\"properties" in a:
            json_string = a.lstrip("window.jsonModel = ")
            f = open("page.json", "w")
            f.write(f"{json_string}")
            f.close()
            break

    # convert json string to dictionary
    with open("page.json") as fp:
        page_dict = json.load(fp)

    # property data is contained in this list of dicts
    properties = page_dict["properties"]

    # establish database connection
    db = sqlite3.connect("properties.db")

    for property in properties:
        
        # for loading screen
        global counter
        counter += 1
        
        # check if property already in db
        cursor = db.execute("SELECT * FROM properties WHERE propertyid=?", [property["id"]])
        row = cursor.fetchone()
        
        # if not
        if not row:

            y = 0

            # download images
            for image in property["propertyImages"]["images"]:
                image_data = [property["id"], image["srcUrl"]]
                cursor_obj = db.cursor()
                cursor_obj.execute("INSERT INTO images (property_id, URL) VALUES(?, ?)", image_data)
                db.commit()
                save(image["srcUrl"], property["id"], y)
                sleep(0.2)
                y += 1
    
            # add property to database
            data = [property["id"], property["bedrooms"], property["bathrooms"], property["numberOfImages"], property["summary"], 
                    property["numberOfFloorplans"], property["price"]["displayPrices"][0]["displayPrice"], property["displayAddress"], 
                    property["location"]["latitude"], property["location"]["longitude"], property["listingUpdate"]["listingUpdateDate"], property["customer"]["branchDisplayName"], property["firstVisibleDate"], 
                    property["addedOrReduced"], new_search_id]
            
            cursor_obj = db.cursor()
            cursor_obj.execute("INSERT or REPLACE INTO properties (propertyid, bedrooms, bathrooms, pics, summary, floorplans, price, address, lattitude, longitude, updateDate, agent, firstVisible, addedOrReduced, search_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
            db.commit()

        i += 1
        
    return page_dict, i


def url_generator(attributes):

    # root URL
    url = "https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier=REGION^475"

    # generate target URL by concatenation
    for attribute in attributes:
        url = url + "&" + attribute + "=" + str(attributes[attribute])

    return url


def save(image_url, id, y):

    # get image
    r = requests.get(image_url)

    # file pointer
    f = f"static/images/{id}/{y}.jpg"

    # check path exists
    if not os.path.exists(os.path.dirname(f)):
        os.makedirs(os.path.dirname(f))

    # save image
    if r.status_code == 200:
        with open(f"static/images/{id}/{y}.jpg", 'wb') as f:
            f.write(r.content)

def convert_html_to_pdf(html, output_file):
    result_file = open(output_file, "w+b")
    pisa_status = pisa.CreatePDF(html, dest=result_file)
    result_file.close()
    return pisa_status.err