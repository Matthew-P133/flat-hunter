import requests
from bs4 import BeautifulSoup
import json

# get page html and write to file
page = requests.get("https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E475&maxBedrooms=3&minBedrooms=2&propertyTypes=&maxDaysSinceAdded=7&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords=")
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

# convert json string to dictionary
with open("page.json") as fp:
    this_dict = json.load(fp)

# property data is contained in this element
properties = this_dict["properties"]

i = 1

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

    # TODO: return this data in a useful form for rest of program

    i += 1
