from helpers import scrape, url_generator
from time import sleep

# TO DO: dynamically pass in attributes
# attributes for testing
attributes = {
    "minBedrooms": 5,
    "maxBedrooms": 7,
    "floorplan": 1,
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
while (pagination["next"] <= pagination["last"]):
    url = url_generator(attributes)
    sleep(5)
    result = scrape(url, i)
    i = result[1]

    page_dict = result[0]
    pagination = page_dict["pagination"]
    if "next" not in pagination.keys():
        break
    attributes["index"] =  pagination["next"]