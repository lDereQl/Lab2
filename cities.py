import requests
from bs4 import BeautifulSoup
import json

def fetch_infobox_data(page_title):
    # Function to fetch infobox data from Wikipedia
    base_url = "https://en.wikipedia.org/wiki/"
    response = requests.get(base_url + page_title)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the infobox table
    infobox_table = soup.find('table', class_='infobox')

    # Extract relevant information from the infobox table
    infobox_data = {
        "type": "Empty",
        "location": "Empty",
        "completed": "Empty",
        "website": "Empty"
    }
    if infobox_table:
        rows = infobox_table.find_all('tr')
        for row in rows:
            header = row.find('th')
            if header:
                header_text = header.text.strip().lower()  # Convert to lowercase for easy comparison
                data = row.find('td')
                if data:
                    data_text = data.text.strip()
                    # Check for relevant fields and update infobox_data
                    if "type" in header_text:
                        infobox_data["type"] = data_text
                    elif "location" in header_text:
                        infobox_data["location"] = data_text
                    elif "completed" in header_text:
                        infobox_data["completed"] = data_text
                    elif "website" in header_text:
                        infobox_data["website"] = data_text

    return infobox_data

def enhance_places_data(city):
    # Function to enhance the collected places data with infobox data
    file_path = f"{city}_places.json"
    enhanced_file_path = f"enhanced_{city}_places.json"

    with open(file_path, 'r', encoding='utf-8') as f:
        places_data = json.load(f)

    for place in places_data:
        page_title = place['title']
        infobox_data = fetch_infobox_data(page_title)
        # Update place with infobox data
        place.update(infobox_data)
        # Add description from Wikipedia page
        place['description'] = fetch_description(page_title)

    with open(enhanced_file_path, 'w', encoding='utf-8') as f:
        json.dump(places_data, f, ensure_ascii=False, indent=4)

    print(f"Enhanced data for {city} places saved to {enhanced_file_path}.")

def fetch_description(page_title):
    # Function to fetch the description (first paragraph) from Wikipedia page
    base_url = "https://en.wikipedia.org/wiki/"
    response = requests.get(base_url + page_title)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find the first paragraph of the Wikipedia page content
    first_paragraph = soup.find('div', class_='mw-parser-output').find('p')
    # Extract text from the paragraph if found, else return "Empty"
    if first_paragraph:
        return first_paragraph.text.strip()
    else:
        return "Empty"

# List of cities to enhance data
cities = ["Berlin", "Stockholm", "Klaipeda", "Tokyo"]

for city in cities:
    enhance_places_data(city)
