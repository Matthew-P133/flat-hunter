from helpers import scrape, url_generator

attributes = {
    "minBedrooms": 5,
    "maxBedrooms": 7,
    "floorplan": 1,
}
i = 1

url = url_generator(attributes)
result = scrape(url, i)
page_dict = result[0]
i = result[1]

index = page_dict["searchParameters"]["index"]
pagination = page_dict["pagination"]
print(pagination["next"])
attributes["index"] =  pagination["next"]

while (pagination["next"] <= pagination["last"]):
    url = url_generator(attributes)
    result = scrape(url, i)
    page_dict = result[0]
    i = result[1]
    pagination = page_dict["pagination"]
    if "next" not in pagination.keys():
        break
    print(pagination["next"])
    attributes["index"] =  pagination["next"]