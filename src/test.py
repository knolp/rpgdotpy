import requests
import json

helenelund = "9507"

query = "http://api.sl.se/api2/deviations.json?key=7d8c88781a3e4118b74106507decf4a8&transportMode=train&siteId=9507"


response = requests.get(query)

data = response.json()

for item in data["ResponseData"]:
    print(item["Details"])
    print("")