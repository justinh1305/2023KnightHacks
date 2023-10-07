import ticketpy
import os
from dotenv import load_dotenv

load_dotenv()
# Define your API key
api_key = os.getenv('API_KEY')
tm_client = ticketpy.ApiClient(api_key)

def get_events(classification_name, state_code, start_date_time, end_date_time):
    pages = tm_client.events.find(
        classification_name=classification_name,
        state_code=state_code,
        start_date_time=start_date_time,
        end_date_time=end_date_time
    )
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
        events[event]['priceRanges'] = events[event]['priceRanges'][0]['min']
    return events

#test = get_events('Hip-Hop', 'GA', '2023-11-19T20:00:00Z', '2023-11-21T20:00:00Z')
#print(test)
