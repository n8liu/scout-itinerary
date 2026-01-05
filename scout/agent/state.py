"""State schema for the Scout travel agent."""
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class TravelState(TypedDict):
    """State schema for multi-step travel planning workflow."""

    messages: Annotated[Sequence[BaseMessage], add_messages]
    destination: str
    dates: dict  # {"start": "2025-03-15", "end": "2025-03-22"}
    budget: dict  # {"flights": 500, "hotels": 1000, "total": 2000}
    travelers: int
    preferences: dict  # {"airline": "any", "hotel_stars": 4, "direct_only": False}
    flight_options: list
    hotel_options: list
    selected_flights: dict
    selected_hotel: dict
    calendar_event_id: str
    stage: str  # "intake" | "research" | "compare" | "finalize" | "complete"
