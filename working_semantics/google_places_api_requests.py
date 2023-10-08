import requests
import os
from dotenv import load_dotenv

load_dotenv()
# Define your API key
api_key = os.getenv('MAPS_KEY')


def getPlace(keyword, location, radius, place_type, place_max, place_min):
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    print(place_type)
    # Define the parameters
    params = {
        'keyword': keyword,
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
    print(len(all_results))
    dict = {}
    c = 0
    for i, establishment in enumerate(all_results):
        if i > 10:
            break
        
        Name = establishment.get('name')
        Price = establishment.get('price_level', 1)
        Rating = establishment.get('rating', 'N/A')
        Reference = establishment.get('reference', 'N/A')

        Geometry = establishment.get('geometry', 'N/A')
        Location = Geometry.get('location', 'N/A')
        Lat = Location.get('lat', 'N/A')
        Lng = Location.get('lng', 'N/A')

        Photos = establishment.get('photos', 'N/A')
        Photo_ID = "N/A"
        for entry in Photos:
            Photo_ID = entry.get('photo_reference', 'N/A')
            break

        dict[c] = {"name": Name, "price_level": Price, "rating": Rating, "reference": Reference, "lat": Lat,
                    "lng": Lng, "photo_reference": Photo_ID}
        c += 1
        print(dict)
        return dict

# dict = getPlace('Main Street', '25.914329725092866, -80.30991221041161', 1500, 'restaurant', 4, 0)
