import json
from semantic_kernel import ContextVariables, Kernel
from semantic_kernel.skill_definition import sk_function
from semantic_kernel.orchestration.sk_context import SKContext
import requests
import os
from dotenv import load_dotenv

load_dotenv()
# Define your API key
api_key = os.getenv('MAPS_KEY')
LAT_LON = ""
def get_context_find_oevents(data):
    context_variables = ContextVariables()
    context_variables["classification_name"] = data["classification_name"]
    context_variables["state_code"] = data["state_code"]
    context_variables["start_date"] = convert_date(data["departure_date"])
    context_variables["end_date"] = convert_date(data["arrival_date"])
    return context_variables

def get_context_find_events(data):
    context_variables = ContextVariables()
    context_variables["event_keyword"] = data["event_keyword"]
    context_variables["state_code"] = data["state_code"]
    context_variables["start_date"] = convert_date(data["departure_date"])
    context_variables["end_date"] = convert_date(data["arrival_date"])
    return context_variables

def get_context_find_hotels(data):
    context_variables = ContextVariables()
    context_variables["hotel_keyword"] = data["hotel_keyword"]
    context_variables["location"] = get_lat_lng(data["location"])
    context_variables["radius"] = DEFAULT_RADIUS
    context_variables["place_max"] = data["budget"]
    context_variables["place_min"] = PLACE_MIN
    return context_variables

def get_context_get_place(data):
    context_variables = ContextVariables()
    context_variables["place_keyword"] = data["place_keyword"]
    context_variables["location"] = get_lat_lng(data["location"])
    context_variables["radius"] = DEFAULT_RADIUS
    context_variables["place_type"] = data["place_type"]
    context_variables["place_max"] = data["budget"]
    context_variables["place_min"] = PLACE_MIN
    return context_variables

DEFAULT_RADIUS = 15000
PLACE_MIN = 0

DATA_MODEL = {
    "FindOEvents": ['classification_name', 'state_code', 'start_date', 'end_date'],
    "FindEvents": ['event_keyword', 'state_code', 'start_date', 'end_date'],
    "FindHotels": ['hotel_keyword', 'location', 'radius', 'place_max', 'place_min'],
    "GetPlace": ['place_keyword', 'location', 'radius', 'place_type', 'place_max', 'place_min'],
}

FUNCTION_MAP = {
    "FindOEvents": get_context_find_oevents,
    "FindEvents": get_context_find_events,
    "FindHotels": get_context_find_hotels,
    "GetPlace": get_context_get_place,
}

def get_lat_lng(city):
    global LAT_LON
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city}&key={api_key}"
    response = requests.get(url).json()
    if response["status"] == "OK":
        lat = response["results"][0]["geometry"]["location"]["lat"]
        lng = response["results"][0]["geometry"]["location"]["lng"]
        LAT_LON = f"{lat},{lng}"
        return f"{lat},{lng}"
    else:
        return None

# convert mm-dd-yyyy to yyyy-mm-dd
def convert_date(date):
    return date[6:10] + '-' + date[0:2] + '-' + date[3:5] + 'T20:00:00Z'



class Orchestrator:
    def __init__(self, kernel: Kernel):
        self._kernel = kernel

    @sk_function(
        description="Routes the request to the appropriate function",
        name="RouteRequest",
    )
    async def route_request(self, context: SKContext) -> str:
        # Save the original user request
        request = context["input"]
        # Add the list of available functions to the context variables
        variables = ContextVariables()
        variables["input"] = request
        variables["options"] = {"ExperiencesPlugin": "FindEvents", "HotelsPlugin": "FindHotels", "PlacesPlugin": "GetPlace"}

        # Retrieve the intent from the user request
        get_intent = self._kernel.skills.get_function("OrchestratorPlugin", "GetIntent")
        intent = (
            await self._kernel.run_async(get_intent, input_vars=variables)
        ).result.strip()

        get_data = self._kernel.skills.get_function(
            "OrchestratorPlugin", "GetUserData"
        )
        getDataContext = (
            await self._kernel.run_async(get_data, input_str=request)
        ).result
        structured_data = json.loads(getDataContext)

        expand_data = self._kernel.skills.get_function(
            "OrchestratorPlugin", "ExpandData"
        )
        expanded_data = (
            await self._kernel.run_async(expand_data, input_str=str(structured_data))
        ).result
        structured_expanded = json.loads(expanded_data)
        structured_data.update(structured_expanded)

        json_data_b = {'type': ['gastronomic', 'music'], 'budget': '3', "place_keyword": "gourmet", "classification_name": "music"}
        balance_place_keywords = self._kernel.skills.get_function(
            "OrchestratorPlugin", "BalancePlaces"
        )

        balanced_place_keywords_context = (
            await self._kernel.run_async(balance_place_keywords, input_str=str(json_data_b))
        )

        res = balanced_place_keywords_context['input']

        balanced_place_keywords = json.loads(res)

        all_results = {}
        for option in variables["options"]:
            current_context = FUNCTION_MAP[variables["options"][option]](structured_data)
            # Call the appropriate function with the user request
            function = self._kernel.skills.get_function(option, variables["options"][option])
            results = await self._kernel.run_async(
                function, input_vars=current_context
            )
            #print(results['input'])
            all_results[option] = results['input']

        all_results['BalancePlaces'] = balanced_place_keywords
        all_results['structured_data'] = structured_data
        all_results['lat_lon'] = LAT_LON
        # write all_results to a json file
        with open('all_results.json', 'w') as fp:
            json.dump(all_results, fp)
        
        return all_results
