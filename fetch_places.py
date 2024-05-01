import requests
import json
import os

def fetch_wikipedia_places(city, centers):
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    max_results = 1000  # Per center
    results = []

    for latitude, longitude in centers:
        params = {
            "action": "query",
            "format": "json",
            "list": "geosearch",
            "gsradius": 10000,  # Maximum radius in meters
            "gscoord": f"{latitude}|{longitude}",
            "gslimit": "500"  # Max limit per request
        }
        while True:
            response = S.get(url=URL, params=params)
            data = response.json()

            if 'query' in data:
                results.extend(data['query']['geosearch'])
                if 'continue' in data:
                    params['gscontinue'] = data['continue']['gscontinue']
                else:
                    break
            else:
                break

        if len(results) >= max_results:
            break

    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, f'{city}_places.json')

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(results[:max_results], f, ensure_ascii=False, indent=4)

    print(f"Collected {len(results)} places for {city}. Data saved to {file_path}.")

cities = {
    "Berlin": [(52.5200, 13.4050), (52.5400, 13.4050)],  # Example additional centers
    "Stockholm": [(59.3293, 18.0686), (59.3493, 18.0686)],
    "Klaipeda": [(55.7033, 21.1443)],
    "Tokyo": [(35.6895, 139.6917), (35.7095, 139.7317)]
}

for city, coords in cities.items():
    fetch_wikipedia_places(city, coords)
