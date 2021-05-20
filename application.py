from helpers import scrape, url_generator

attributes = {
    "bedrooms": 1,
    "floorplan": 1,
}

url = url_generator(attributes)

scrape(url)