import weather_api_call
from semantic_kernel.skill_definition import (
    sk_function,
    sk_function_context_parameter,
)
from semantic_kernel.orchestration.sk_context import SKContext

class Weather:
    @sk_function(
        description="Finds the weather based on the latitude and longitude",
        name="FindWeather",
        input_description="The latitude and longitude",
    )
    @sk_function_context_parameter(
        name="latitude",
        description="The latitude of the location",
    )
    @sk_function_context_parameter(
        name="longitude",
        description="The longitude of the location",
    )
    def find_weather(self, context: SKContext) -> str:
        return str(weather_api_call.getWeather(context["latitude"], context["longitude"]))