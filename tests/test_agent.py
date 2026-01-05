"""Tests for Scout agent workflow."""
import pytest
from scout.agent.state import TravelState
from scout.agent.nodes import should_use_tools
from langchain_core.messages import HumanMessage, AIMessage


def test_travel_state_schema():
    """Test that TravelState has expected fields."""
    state: TravelState = {
        "messages": [HumanMessage(content="Test")],
        "destination": "Tokyo",
        "dates": {"start": "2025-03-15", "end": "2025-03-22"},
        "budget": {"total": 3000},
        "travelers": 2,
        "preferences": {},
        "flight_options": [],
        "hotel_options": [],
        "selected_flights": {},
        "selected_hotel": {},
        "calendar_event_id": "",
        "stage": "intake",
    }

    assert state["destination"] == "Tokyo"
    assert state["travelers"] == 2
    assert state["stage"] == "intake"


def test_should_use_tools_no_tools():
    """Test routing when no tool calls are present."""
    state: TravelState = {
        "messages": [AIMessage(content="Hello")],
        "destination": "",
        "dates": {},
        "budget": {},
        "travelers": 1,
        "preferences": {},
        "flight_options": [],
        "hotel_options": [],
        "selected_flights": {},
        "selected_hotel": {},
        "calendar_event_id": "",
        "stage": "research",
    }

    result = should_use_tools(state)
    assert result == "compare"


# More comprehensive tests would require mocking the LLM
