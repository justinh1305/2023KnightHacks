import google_places_api_requests
from semantic_kernel.skill_definition import (
    sk_function,
    sk_function_context_parameter,
)
from semantic_kernel.orchestration.sk_context import SKContext


class Places:
    @sk_function(
        description="Finds a list of places based on keyword, location, radius, type, max, min",
        name="GetPlace",
        input_description="The keyword, location, radius, type, max, min",
    )
    @sk_function_context_parameter(
        name="place_keyword",
        description="The keyword of the location",
    )
    @sk_function_context_parameter(
        name="location",
        description="The string of the latitude and longitude of the location. (ex. '25.914329725092866, -80.30991221041161')",
    )
    @sk_function_context_parameter(
        name="radius",
        description="The search radius of the location in meters",
    )
    @sk_function_context_parameter(
        name="place_type",
        description="The type of the location (restaurant, bar, etc.)",
    )
    @sk_function_context_parameter(
        name="place_max",
        description="The maximum price level of the location from 0-4",
    )
    @sk_function_context_parameter(
        name="place_min",
        description="The minimum price level of the location from 0-4",
    )
    def getPlace(self, context: SKContext) -> str:
        return str(google_places_api_requests.getPlace(context["place_keyword"], context["location"], context["radius"],
                                                       context["place_type"], context["place_max"],
                                                       context["place_min"]))
