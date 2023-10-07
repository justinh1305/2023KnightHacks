
from amadeus import Client, ResponseError
import os
from dotenv import load_dotenv

load_dotenv()
# Defines API key
CID = os.getenv('CLIENT_ID')
CIS = os.getenv('CLIENT_SECRET')

amadeus = Client(client_id=CID, client_secret=CIS)

# Function that creates a dictionary out of valuable information from the API call
def flight_input(originLocCode, destinationLocCode,departureD,people,maxBudget):
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode = originLocCode,
            destinationLocationCode = destinationLocCode,
            departureDate= departureD,
            adults= people,
            maxPrice = maxBudget
    )

        info_dict = {}
        for i, flight in enumerate(response.data):
                last_ticketing_date = flight["lastTicketingDate"]
                number_of_seats = flight["numberOfBookableSeats"]
                itinerary_dict = flight["itineraries"]
                price_dict = flight["price"]
                traveler_pricing_dict = flight["travelerPricings"]
                info_dict[i] = {"id":flight["id"],"last_ticketing_date": last_ticketing_date, "number_of_seats": number_of_seats, "itinerary": itinerary_dict, "price": price_dict, "traveler_pricing": traveler_pricing_dict}
                
        print(info_dict)
        return info_dict

    except ResponseError as error:
        print(error)

# flight_input("MAD","ATH","2023-11-01",1,500)
