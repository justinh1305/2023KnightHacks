import ticketpy
import os
from dotenv import load_dotenv

load_dotenv()
# Define your API key
api_key = os.getenv('API_KEY')
tm_client = ticketpy.ApiClient(api_key)

def get_events_discovery(classification_name, state_code, start_date_time, end_date_time):
    print("Inside events discovery")
    print(classification_name, state_code, start_date_time, end_date_time)
    pages = tm_client.events.find(
        classification_name=classification_name,
        state_code=state_code,
        start_date_time=start_date_time,
        end_date_time=end_date_time
    )
    print(pages)
    # Turn response into a dictionary
    events = {}
    for page in pages:
        for event in page:
            events[event.name] = event.json

    # Remove all unneccessary keys but: name, type, images, sales, dates, and priceRanges
    for event in events:
        events[event] = {k: events[event][k] for k in ('name', 'type', 'images', 'sales', 'dates', 'priceRanges')}
        events[event]['images'] = events[event]['images'][0]['url']
        events[event]['sales'] = events[event]['sales']['public']['startDateTime']
        events[event]['dates'] = events[event]['dates']['start']['localDate']
        #events[event]['priceRanges'] = events[event]['priceRanges'][0]
    
    print(events)
    return events



import requests

def extract_event_info(response):
    # Check if '_embedded' key exists in the response
    if '_embedded' not in response:
        print("No events found.")
        return []

    events = response['_embedded']['events']

    # Initialize an empty list to store the extracted event info
    event_info = []

    for event in events:
        # Extract the desired fields
        name = event.get('name')
        type = event.get('type')
        images = event.get('images', [{}])[0].get('url')  # Get the URL of the first image
        sales = event.get('sales', {}).get('public', {}).get('startDateTime')
        dates = event.get('dates', {}).get('start', {}).get('localDate')
        priceRanges = event.get('priceRanges', [{}])[0]

        # Add the extracted info to the list
        event_info.append({
            'name': name,
            'type': type,
            'images': images,
            'sales': sales,
            'dates': dates,
            'priceRanges': priceRanges,
        })

    return event_info

def search_events(keyword, state_code, start_date_time, end_date_time):
    url = f'https://app.ticketmaster.com/discovery/v2/events.json'
    params = {
        'keyword': keyword,
        'apikey': api_key,
        'stateCode': state_code,
        'startDateTime': start_date_time,
        'endDateTime': end_date_time
    }
    response = requests.get(url, params=params)
    return extract_event_info(response.json())




#test2 = search_events('Doja Cat', 'GA', '2023-11-19T20:00:00Z', '2023-11-21T20:00:00Z')
#test2 = extract_event_info(test2)
#print(test2)
#test = get_events_discovery('Hip-Hop', 'GA', '2023-11-19T20:00:00Z', '2023-11-21T20:00:00Z')
#print(test)
