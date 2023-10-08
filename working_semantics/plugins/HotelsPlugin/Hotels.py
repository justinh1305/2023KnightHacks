import hotel_requests

from semantic_kernel.skill_definition import(
    sk_function,
    sk_function_context_parameter,
)
from semantic_kernel.orchestration.sk_context import SKContext

class Hotels:
    @sk_function(
        description="Finds hotels based on the keyword, location, search radius, max price bracket, and min price bracket",
        name="FindHotels",
        input_description="The keyword, location, radisu, place_max, and place_min",
    )
    @sk_function_context_parameter(
        name="keyword",
        description="The keyword of the hotel",
    )
    @sk_function_context_parameter(
        name="location",
        description="The location of the hotel in latitude and longitude (ex. 33.7490, -84.3880)",
    )
    @sk_function_context_parameter(
        name="radius",
        description="The radius of the search area for hotels in meters (ex. 10000)",
    )
    @sk_function_context_parameter(
        name="place_max",
        description="The maximum price bracket of the hotel (0-4)",
    )
    @sk_function_context_parameter(
        name="place_min",
        description="The minimum price bracket of the hotel (0-4)",
    )
    def FindHotels(self, context: SKContext) -> str:
        return str(hotel_requests.getHotel(context["keyword"], context["location"], context["place_max"],
                                                      context["place_min"]))