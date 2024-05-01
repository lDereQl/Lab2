import json
import csv

def create_csv(city):
    # Define the input file path
    input_file = f"enhanced_{city}_places.json"

    # Open the input JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data

# List of cities to process
cities = ["Berlin", "Stockholm", "Klaipeda", "Tokyo"]

# List to hold all data
all_data = []

# Process each city
for city in cities:
    city_data = create_csv(city)
    for place in city_data:
        # Add the city name to each place data
        place["City"] = city
    all_data.extend(city_data)

# Define the output file path
output_file = "all_places.csv"

# Define the fieldnames for the CSV file
fieldnames = ["City", "pageid", "ns", "title", "lat", "lon", "dist", "primary", "type", "location", "completed", "website"]

# Open the output CSV file in write mode
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write the data to the CSV file
    for place in all_data:
        writer.writerow({
            "City": place.get("City", ""),
            "pageid": place.get("pageid", ""),
            "ns": place.get("ns", ""),
            "title": place.get("title", ""),
            "lat": place.get("lat", ""),
            "lon": place.get("lon", ""),
            "dist": place.get("dist", ""),
            "primary": place.get("primary", ""),
            "type": place.get("type", ""),
            "location": place.get("location", ""),
            "completed": place.get("completed", ""),
            "website": place.get("website", "")
        })

print(f"CSV file containing data for all cities created: {output_file}")
