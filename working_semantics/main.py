import semantic_kernel as sk

from plugins.MathPlugin.Math import Math
from plugins.HotelsPlugin.Hotels import Hotels
from plugins.ExperiencesPlugin.Experiences import Experiences
from plugins.PlacesPlugin.Places import Places
from plugins.WeatherPlugin.Weather import Weather

from plugins.OrchestratorPlugin.Orchestrator import Orchestrator
from semantic_kernel.core_skills import ConversationSummarySkill

from semantic_kernel.connectors.ai.open_ai import (
    AzureTextCompletion,
    OpenAITextCompletion,
)
from semantic_kernel.orchestration.context_variables import ContextVariables


async def main():
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
    experiences_plugin = kernel.import_skill(Hotels(), skill_name="HotelsPlugin")
    experiences_plugin = kernel.import_skill(Experiences(), skill_name="ExperiencesPlugin")
    places_plugin = kernel.import_skill(Places(), skill_name="PlacesPlugin")
    weather_plugin = kernel.import_skill(Weather(), skill_name="WeatherPlugin")

    orchestrator_plugin = kernel.import_skill(
        Orchestrator(kernel), skill_name="OrchestratorPlugin"
    )

    result1 = await kernel.run_async(
        orchestrator_plugin["RouteRequest"],
        input_str="['Going to Seattle on the 11th of July, 2025', 'Traveling with a party of 5', 'Interested in a gastronomic and music oriented trip', 'Hoping to come back on the 21st', 'Our budget is moderately high']",
    )
    print(result1)

    # Make a request that runs the Sqrt function.
    # result1 = await kernel.run_async(
    #     orchestrator_plugin["RouteRequest"],
    #     input_str="What is the square root of 634?",
    # )
    # print(result1)

    # # Make a request that runs the Multiply function.
    # result2 = await kernel.run_async(
    #     orchestrator_plugin["RouteRequest"],
    #     input_str="What is 12.34 times 56.78?",
    # )
    # print(result2)


# Run the main function
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())