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
    @sk_function(
        name="Classification Name",
        description="The category name of the event",
    )
    @sk_function(
        name="State Code",
        description="The state code of the event (ex. Georgia as \"GA\")",
    )
    @sk_function(
        name="Start Date",
        description="The start date of the event formatted in ISO 8601  (ex. 2023-11-19T20:00:00Z)",
    )
    @sk_function(
        name="End Date",
        description="The end date of the event formatted in ISO 8601  (ex. 2023-11-21T20:00:00Z)",
    )
    def find_events(self, classification_name: str, state_code: str, start_date_time: str, end_date_time: str) -> str:
        return str(
            ticketmaster_api_call.get_events_discovery(classification_name, state_code, start_date_time, end_date_time))

    @sk_function(
        description="Finds events based on the keyword, state code, start date, and end date",
        name="Find Events",
        input_description="The keyword, state code, start date, and end date",
    )
    @sk_function(
        name="Keyword",
        description="The keyword of the event",
    )
    @sk_function(
        name="State Code",
        description="The state code of the event (ex. Georgia as \"GA\")",
    )
    @sk_function(
        name="Start Date",
        description="The start date of the event formatted in ISO 8601  (ex. 2023-11-19T20:00:00Z)",
    )
    @sk_function(
        name="End Date",
        description="The end date of the event formatted in ISO 8601  (ex. 2023-11-21T20:00:00Z)",
    )
    def find_events(self, keyword: str, state_code: str, start_date_time: str, end_date_time: str) -> str:
        return str(ticketmaster_api_call.get_events_discovery(keyword, state_code, start_date_time, end_date_time))
