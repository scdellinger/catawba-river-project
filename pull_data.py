import requests
import json
import pandas as pd

url = "https://api.waterdata.usgs.gov/ogcapi/v0/collections/daily/items"
params = {
    "f": "json",
    "monitoring_location_id": "USGS-02137727",
    "parameter_code": "00065, 00060, 00010",   # Gauge height: 00065, discharge: 00060, temperature: 00010
    "time": "1987-11-11T00:00:00Z/2025-12-31T00:00:00Z",
    "limit": 10000
}

all_features = []
current_url = url
current_params = params

while True:

    response = requests.get(current_url, params=current_params)
    current_params = None
    data = response.json()
    all_features += data['features']

    next_found = False

    for link in data['links']:
        if link['rel'] == 'next':
            current_url = link['href']
            next_found = True
            break
    if next_found == False:
        break

with open('ras_data.json', 'w') as f:
    json.dump(all_features, f)


