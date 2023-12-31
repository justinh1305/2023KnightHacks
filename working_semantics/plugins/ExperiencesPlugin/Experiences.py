import ticketmaster_api_call
from semantic_kernel.skill_definition import (
    sk_function,
    sk_function_context_parameter,
)
from semantic_kernel.orchestration.sk_context import SKContext


class Experiences:
    @sk_function(
        description="Finds events based on the classification name, state code, start date, and end date",
        name="FindOEvents",
        input_description="The classification name, state code, start date, and end date",
    )
    @sk_function_context_parameter(
        name="classification_name",
        description="The category name of the event",
    )
    @sk_function_context_parameter(
        name="state_code",
        description="The state code of the event (ex. Georgia as \"GA\")",
    )
    @sk_function_context_parameter(
        name="start_date",
        description="The start date of the event formatted in ISO 8601  (ex. 2023-11-19T20:00:00Z)",
    )
    @sk_function_context_parameter(
        name="end_date",
        description="The end date of the event formatted in ISO 8601  (ex. 2023-11-21T20:00:00Z)",
    )
    def find_oevents(self, context: SKContext) -> str:
        return str(
            ticketmaster_api_call.get_events_discovery(context["classification_name"], context["state_code"],
                                                       context["start_date"], context["end_date"]))

    @sk_function(
        description="Finds events based on the keyword, state code, start date, and end date",
        name="FindEvents",
        input_description="The keyword, state code, start date, and end date",
    )
    @sk_function_context_parameter(
        name="event_keyword",
        description="The keyword of the event",
    )
    @sk_function_context_parameter(
        name="state_code",
        description="The state code of the event (ex. Georgia as \"GA\")",
    )
    @sk_function_context_parameter(
        name="start_date",
        description="The start date of the event formatted in ISO 8601  (ex. 2023-11-19T20:00:00Z)",
    )
    @sk_function_context_parameter(
        name="end_date",
        description="The end date of the event formatted in ISO 8601  (ex. 2023-11-21T20:00:00Z)",
    )
    def find_events(self, context: SKContext) -> str:
        return str(ticketmaster_api_call.search_events(context["event_keyword"], context["state_code"],
                                                              context["start_date"], context["end_date"]))
