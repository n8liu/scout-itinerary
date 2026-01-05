"""Tests for Scout tools."""
import pytest
from scout.tools.flights import search_flights
from scout.tools.hotels import search_hotels


def test_search_flights_signature():
    """Test that search_flights has the correct signature."""
    # This test validates the tool can be called
    # Actual API calls would require API keys
    assert callable(search_flights)
    assert search_flights.name == "search_flights"


def test_search_hotels_signature():
    """Test that search_hotels has the correct signature."""
    assert callable(search_hotels)
    assert search_hotels.name == "search_hotels"


def test_search_hotels_mock_data():
    """Test that search_hotels returns mock data when API key not configured."""
    result = search_hotels.invoke(
        {
            "destination": "Tokyo",
            "checkin": "2025-03-15",
            "checkout": "2025-03-22",
            "guests": 2,
        }
    )

    assert "hotels" in result
    assert len(result["hotels"]) > 0
    assert all("price_per_night" in h for h in result["hotels"])
    assert all("name" in h for h in result["hotels"])


# Add more tests as needed
# Real API tests would require valid API keys and should be integration tests
