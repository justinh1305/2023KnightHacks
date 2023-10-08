import requests
import json

def getWeather(lat, long):
    url = "https://api.weather.gov/points/" + str(lat) + "," + str(long)
    response = requests.get(url)
    data = json.loads(response.text)
    forecast_url = data['properties']['forecast']
    forecast_response = requests.get(forecast_url)
    forecast_data = json.loads(forecast_response.text)
    forecast = {}

    for period in forecast_data['properties']['periods']:
        # Split the name string into a list of words
        name_words = period['name'].split()

        # If the first word is 'This', remove it
        if name_words[0] == 'This':
            name_words.pop(0)

        # Join the remaining words back into a string and use it as the key
        key = ' '.join(name_words)

        # Add the forecast to the dictionary
        forecast[key] = period['shortForecast']

    return forecast

#test = getWeather(28.60107, -81.19949)
#print(test)
