import requests
import os
from dotenv import load_dotenv

load_dotenv()
# Define your API key
api_key = os.getenv('MAPS_KEY')

def getJson(name):
    # Define the Find Places endpoint URL
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'

    # Define the parameters
    params = {
        'fields': 'formatted_address,opening_hours',
        'input': name,
        'inputtype': 'textquery',
        'key': api_key
    }

    # Make the API request
    response = requests.get(url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        # Access and work with the response data as needed
        if 'opening_hours' in data['candidates'][0]:
            opening_hours = data['candidates'][0]['opening_hours']

            if 'weekday_text' in opening_hours:
                for day, hours in opening_hours['weekday_text']:
                    print(f"{day}: {hours}")
            else:
                print("No specific opening hours available.")
        else:
            print("Opening hours not available for this place.")
    else:
        print('Error:', response.status_code)
    print(data)

getJson("Thai Cafe Miami Lakes")
