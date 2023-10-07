import requests
import os
from dotenv import load_dotenv

load_dotenv()
# Define your API key
api_key = os.getenv('MAPS_KEY')

def getJson(keyword, location, radius, type, max, min):
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

    # Define the parameters
    params = {
        'keyword':keyword,
        'location':location,
        'radius': radius,
        'type':type,
        'maxPrice':max,
        'minPrice':min,
        'key': api_key
    }

    # Make the API request
    response = requests.get(url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()

        # Access the response data as needed
        #print(data)
    else:
        print('Error:', response.status_code)
    
    all_results = data.get("results")
    dict = {}
    for i, establishment in enumerate(all_results):
        #Conditional excludes any establishments that do not have all values listed, in doing so it also skips indexes.
        #For example, if index 2 is missing the price level, the conditional will skip 2 entirely and print indexes 0, 1, 3, ...
        if 'name' in establishment and 'price_level' in establishment and 'rating' in establishment and 'reference' in establishment and 'geometry' in establishment and 'photos' in establishment:
            Name = establishment['name']
            Price = establishment['price_level']
            Rating = establishment['rating']
            Reference = establishment['reference']

            Geometry = establishment['geometry']
            Location = Geometry['location']
            Lat = Location['lat']
            Lng = Location['lng']

            Photos = establishment['photos']
            for entry in Photos:
                Photo_ID = entry['photo_reference']

            dict[i] = {"name":Name, "price_level":Price, "rating":Rating, "reference": Reference, "lat":Lat, "lng":Lng, "photo_reference":Photo_ID}

            print(dict)

getJson('Main Street', '25.914329725092866, -80.30991221041161', 1500, 'restaurant', 4, 0)