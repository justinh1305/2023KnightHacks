import requests
import os
from dotenv import load_dotenv

load_dotenv()
# Define your API key
api_key = os.getenv('MAPS_KEY')


def getPlace(keyword, location, radius, place_max, place_min):
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

    # Define the parameters
    params = {
        'keyword': 'hotel ' + keyword,
        'location': location,
        'radius': radius,
        'maxPrice': place_max,
        'minPrice': place_min,
        'key': api_key
    }

    # Make the API request
    response = requests.get(url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()

        # Access the response data as needed
        # print(data)
    else:
        print('Error:', response.status_code)

    all_results = data.get("results")
    dict = {}
    for i, establishment in enumerate(all_results):
        Name = establishment['name']
        Rating = establishment['rating']
        Reference = establishment['reference']

        Geometry = establishment['geometry']
        Location = Geometry['location']
        Lat = Location['lat']
        Lng = Location['lng']

        Photos = establishment['photos']
        for entry in Photos:
            Photo_ID = entry['photo_reference']

        dict[i] = {"name": Name, "rating": Rating, "reference": Reference, "lat": Lat,
                    "lng": Lng, "photo_reference": Photo_ID}

        # print(dict)
    return dict

# dict = getPlace('University of Central Florida', "28.603810425539493, -81.20049773806359", 1500, 4, 0)
# print(dict)
