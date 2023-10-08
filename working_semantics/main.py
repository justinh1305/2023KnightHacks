import semantic_kernel as sk
from flask import Flask, jsonify, request
import asyncio
import json
import google_places_api_requests
import random

from plugins.MathPlugin.Math import Math
from plugins.HotelsPlugin.Hotels import Hotels
from plugins.ExperiencesPlugin.Experiences import Experiences
from plugins.PlacesPlugin.Places import Places
from plugins.WeatherPlugin.Weather import Weather
import datetime
from plugins.OrchestratorPlugin.Orchestrator import Orchestrator
from semantic_kernel.core_skills import ConversationSummarySkill

from semantic_kernel.connectors.ai.open_ai import (
    AzureTextCompletion,
    OpenAITextCompletion,
)
from semantic_kernel.orchestration.context_variables import ContextVariables


app = Flask(__name__)

@app.route('/initiate-plan', methods=['POST'])
def initiate_plan():
    input_str = request.json.get('input_str', "['Going to Seattle on the 11th of Oct, 2023', 'Traveling with a party of 5', 'Interested in a gastronomic and music oriented trip', 'Hoping to come back on the 21st', 'Our budget is moderately high']")
    asyncio.run(main(input_str))
    build_itinerary()
    return jsonify([])

def convert_date(date):
    return date[6:10] + '-' + date[0:2] + '-' + date[3:5]

def build_itinerary():
    with open('all_results.json') as f:
        all_results = json.load(f)
    
    gmaps_balance = all_results['BalancePlaces']
    structured_data = all_results['structured_data']

    departure_date = datetime.datetime.strptime("10-11-2023", "%m-%d-%Y")
    arrival_date = datetime.datetime.strptime("10-16-2023", "%m-%d-%Y")
    days_in_trip = (arrival_date - departure_date).days

    complete_itin = []
    for i in range(days_in_trip):
        daily_itin = ['restaurant']
        for each_keywork in gmaps_balance:
            if each_keywork == 'restaurant':
                continue
            else:
                if len(daily_itin) < 6 and random.randint(0, 2) == 1:
                    daily_itin.append(each_keywork)
    
        daily_itin.append('restaurant')
        complete_itin.append(daily_itin)
    
    print(complete_itin)
    index_tracker = {}
    response_cache = {}
    itinerary_with_establishments = []
    for each_day in complete_itin:
        daily_establishments = []
        for each_keyword in each_day:
            if each_keyword not in index_tracker:
                index_tracker[each_keyword] = 0
            if each_keyword not in response_cache:
                response_cache[each_keyword] = google_places_api_requests.getPlace(each_keyword, all_results['lat_lon'], 30000, '', structured_data['budget'], 0)
                print(response_cache[each_keyword])
            if response_cache[each_keyword] != None:
                if index_tracker[each_keyword] in response_cache[each_keyword]:
                    daily_establishments.append(response_cache[each_keyword][index_tracker[each_keyword]])
                else:
                    index_tracker[each_keyword] = 0
                    daily_establishments.append(response_cache[each_keyword][index_tracker[each_keyword]])
            index_tracker[each_keyword] += 1
        itinerary_with_establishments.append(daily_establishments)
    print(itinerary_with_establishments)
    
async def main(input_str):
    # Initialize the kernel
    kernel = sk.Kernel()
    # Add a text or chat completion service using either:
    # kernel.add_text_completion_service()
    # kernel.add_chat_service()
    api_key, org_id = sk.openai_settings_from_dot_env()
    kernel.add_text_completion_service(
        "dv", OpenAITextCompletion("text-davinci-003", api_key, org_id)
    )

    plugins_directory = "./plugins"

    # Import the semantic functions
    kernel.import_semantic_skill_from_directory(plugins_directory, "OrchestratorPlugin")
    kernel.import_skill(
        ConversationSummarySkill(kernel=kernel), skill_name="ConversationSummarySkill"
    )

    # Import the native functions.
    math_plugin = kernel.import_skill(Math(), skill_name="MathPlugin")
    hotels_plugin = kernel.import_skill(Hotels(), skill_name="HotelsPlugin")
    experiences_plugin = kernel.import_skill(Experiences(), skill_name="ExperiencesPlugin")
    places_plugin = kernel.import_skill(Places(), skill_name="PlacesPlugin")

    orchestrator_plugin = kernel.import_skill(
        Orchestrator(kernel), skill_name="OrchestratorPlugin"
    )

    result1 = await kernel.run_async(
        orchestrator_plugin["RouteRequest"],
        input_str=input_str,
    )




# Run the main function
if __name__ == "__main__":
    app.run()