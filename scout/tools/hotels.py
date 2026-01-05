"""Hotel search tool."""
from langchain_core.tools import tool
from typing import Optional
import httpx
import os


@tool
def search_hotels(
    destination: str,
    checkin: str,
    checkout: str,
    guests: int = 2,
    min_stars: int = 3,
    max_price_per_night: Optional[int] = None,
) -> dict:
    """Search hotel availability using Skyscanner API.

    Args:
        destination: City name or airport code
        checkin: Format YYYY-MM-DD
        checkout: Format YYYY-MM-DD
        guests: Number of guests
        min_stars: Minimum star rating (1-5)
        max_price_per_night: Maximum nightly rate in USD

    Returns:
        dict with "hotels" list containing name, price, rating, amenities
    """
    api_key = os.getenv("SKYSCANNER_API_KEY")
    if not api_key:
        # Fallback to mock data for development
        return {
            "hotels": [
                {
                    "name": "Sample Hotel Tokyo",
                    "price_per_night": 150,
                    "total_price": 1050,
                    "stars": 4,
                    "rating": 4.5,
                    "amenities": ["WiFi", "Pool", "Gym", "Restaurant"],
                    "location": destination,
                },
                {
                    "name": "Budget Stay Tokyo",
                    "price_per_night": 80,
                    "total_price": 560,
                    "stars": 3,
                    "rating": 4.0,
                    "amenities": ["WiFi", "Breakfast"],
                    "location": destination,
                },
                {
                    "name": "Luxury Hotel Tokyo",
                    "price_per_night": 300,
                    "total_price": 2100,
                    "stars": 5,
                    "rating": 4.8,
                    "amenities": ["WiFi", "Pool", "Gym", "Spa", "Restaurant", "Bar"],
                    "location": destination,
                },
            ]
        }

    # Real Skyscanner API implementation would go here
    try:
        # Placeholder for actual API call
        params = {
            "destination": destination,
            "checkin": checkin,
            "checkout": checkout,
            "guests": guests,
        }
        # response = httpx.get("https://api.skyscanner.net/hotels/...", params=params)
        return {"error": "Skyscanner API integration pending"}
    except Exception as e:
        return {"error": f"Failed to search hotels: {str(e)}"}
