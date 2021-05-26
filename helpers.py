import requests
from bs4 import BeautifulSoup
import json
import sqlite3

def scrape(url, i):
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
        y = str(tag.string)
        if "window.jsonModel = {\"properties" in y:
            json_string = y.lstrip("window.jsonModel = ")
            f = open("page.json", "w")
            f.write(f"{json_string}")
            f.close()
            break

    # convert json string to dictionary
    with open("page.json") as fp:
        page_dict = json.load(fp)

    # property data is contained in this element
    properties = page_dict["properties"]

    db = sqlite3.connect("properties.db")

    # print various data for each property
    for property in properties:
        print("PROPERTY : {}".format(i))
        print("bedrooms : {}".format(property["bedrooms"]))
        print("bathrooms : {}".format(property["bathrooms"]))
        print("pics : {}".format(property["numberOfImages"]))
        print("floorplans : {}".format(property["numberOfFloorplans"]))
        print("summary: {}".format(property["summary"]))
        print("location : {}".format(property["displayAddress"]))
        print("price : {}".format(property["price"]["displayPrices"][0]["displayPrice"]), end="\n\n")

        # add image URLs to database
        for image in property["propertyImages"]["images"]:
            image_data = [property["id"], image["srcUrl"]]
            cursor_obj = db.cursor()
            cursor_obj.execute("INSERT INTO images (property_id, URL) VALUES(?, ?)", image_data)
            db.commit()
            print(image["srcUrl"])

        data = [property["id"], property["bedrooms"], property["bathrooms"], property["numberOfImages"], property["summary"], 
                property["numberOfFloorplans"], property["price"]["displayPrices"][0]["displayPrice"], property["displayAddress"], 
                property["location"]["latitude"], property["location"]["longitude"], property["listingUpdate"]["listingUpdateDate"], property["customer"]["branchDisplayName"], property["firstVisibleDate"], 
                property["addedOrReduced"]]
        
        # add property data to database
        cursor_obj.execute("INSERT or REPLACE INTO properties (propertyid, bedrooms, bathrooms, pics, summary, floorplans, price, address, lattitude, longitude, updateDate, agent, firstVisible, addedOrReduced) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
        db.commit()
        i += 1
    return page_dict, i

def url_generator(attributes):

    url = "https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier=REGION^475"

    for attribute in attributes:
        url = url + "&" + attribute + "=" + str(attributes[attribute])
    return url