import google_places_api_requests
from semantic_kernel.skill_definition import (
    sk_function,
    sk_function_context_parameter,
)
from semantic_kernel.orchestration.sk_context import SKContext

class Place:
    @sk_function(
    description="Finds a list of places based on keyword, location, radius, type, max, min",
    name="Get Place",
    input_description="The keyword, location, radius, type, max, min",
    )
    @sk_function(
        name="Keyword",
        description="The keyword of the location",
    )
    @sk_function(
        name="Location",
        description="The string of the latitude and longitude of the location. (ex. '25.914329725092866, -80.30991221041161')",
    )
    @sk_function(
        name="Radius",
        description="The search radius of the location in meters",
    )
    @sk_function(
        name="Type",
        description="The type of the location (restaurant, bar, etc.)",
    )
    @sk_function(
        name="Max",
        description="The maximum price level of the location from 0-4",
    )
    @sk_function(
        name="Min",
        description="The minimum price level of the location from 0-4",
    )
    def getPlace(self, latitude: str, longitude: str) -> str:
        return str(google_places_api_requests.getPlace(latitude, longitude))
