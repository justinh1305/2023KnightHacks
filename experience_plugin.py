import ticketmaster_api_call
from semantic_kernel.skill_definition import (
    sk_function,
    sk_function_context_parameter,
)
from semantic_kernel.orchestration.sk_context import SKContext


class Experience:
    @sk_function(
        description="Finds events based on the classification name, state code, start date, and end date",
        name="Find Events",
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
    def find_events(self, context: SKContext) -> str:
        return str(
            ticketmaster_api_call.get_events_discovery(context["classification_name"], context["state_code"],
                                                       context["start_date_time"], context["end_date_time"]))

    @sk_function(
        description="Finds events based on the keyword, state code, start date, and end date",
        name="Find Events",
        input_description="The keyword, state code, start date, and end date",
    )
    @sk_function_context_parameter(
        name="keyword",
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
        return str(ticketmaster_api_call.get_events_discovery(context["keyword"], context["state_code"],
                                                              context["start_date_time"], context["end_date_time"]))
