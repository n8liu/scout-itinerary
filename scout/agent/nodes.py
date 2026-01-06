"""Node functions for the Scout travel agent workflow."""
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from .state import TravelState
import os


def get_model_with_tools():
    """Get the LLM model with tools bound."""
    from langchain_google_genai import ChatGoogleGenerativeAI
    from scout.tools import (
        search_flights,
        search_hotels,
        create_trip_event,
        store_preference,
        recall_preferences,
        add_itinerary_item,
        list_trips
    )

    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )
    tools = [
        search_flights,
        search_hotels,
        create_trip_event,
        store_preference,
        recall_preferences,
        add_itinerary_item,
        list_trips
    ]
    return model.bind_tools(tools)


def intake_node(state: TravelState) -> dict:
    """Extract travel requirements from user input."""
    messages = state["messages"]
    model = get_model_with_tools()

    system_message = SystemMessage(
        content="""Extract travel details from the user's request:
        - Destination (city/country)
        - Dates (start and end)
        - Budget (total or per-category)
        - Number of travelers
        - Preferences (airline, hotel class, direct flights, etc.)

        If any required info is missing, ask clarifying questions.
        Be conversational and helpful."""
    )

    response = model.invoke([system_message] + list(messages))

    return {"messages": [response], "stage": "research"}


def research_node(state: TravelState) -> dict:
    """Search for flights and hotels using tools."""
    model = get_model_with_tools()

    system_message = SystemMessage(
        content="""You are researching travel options.
        Use search_flights and search_hotels tools to find options within budget.
        First recall any stored user preferences with recall_preferences.
        Search for 3-5 flight options and 3-5 hotel options.

        After gathering options, summarize what you found and prepare to present them."""
    )

    response = model.invoke([system_message] + list(state["messages"]))

    return {"messages": [response]}


def should_use_tools(state: TravelState) -> str:
    """Route to tools if model requested tool calls."""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "compare"


def compare_node(state: TravelState) -> dict:
    """Present options and help user choose."""
    model = get_model_with_tools()

    system_message = SystemMessage(
        content="""Present the flight and hotel options clearly:

        Format each option with:
        - Price and value comparison
        - Key features (stops, duration, amenities)
        - Your recommendation based on their preferences

        Ask which options they'd like to book."""
    )

    response = model.invoke([system_message] + list(state["messages"]))

    return {"messages": [response], "stage": "finalize"}


def finalize_node(state: TravelState) -> dict:
    """Create calendar event and confirm booking details."""
    model = get_model_with_tools()

    system_message = SystemMessage(
        content="""Finalize the trip:
        1. Summarize selected flights and hotel
        2. Use create_trip_event to add to their calendar
        3. Store any new preferences with store_preference
        4. Provide booking links and next steps"""
    )

    response = model.invoke([system_message] + list(state["messages"]))

    return {"messages": [response], "stage": "complete"}
