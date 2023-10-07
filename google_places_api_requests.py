import requests
import os
from dotenv import load_dotenv

load_dotenv()
# Define your API key
api_key = os.getenv('MAPS_KEY')

# Define the Place Details endpoint URL
url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

# Define the parameters
params = {
    'keyword':'restaurant',
    'location':'28.60107,-81.19949',
    'radius': '1500',
    'type':'restaurant',
    'key': api_key
}

# Make the API request
response = requests.get(url, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    data = response.json()
    # Access the response data as needed
    print(data)
else:
    print('Error:', response.status_code)
