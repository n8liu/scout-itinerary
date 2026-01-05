"""Flight search tool using SerpApi Google Flights."""
from langchain_core.tools import tool
from typing import Optional
import httpx
import os


@tool
def search_flights(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: Optional[str] = None,
    adults: int = 1,
    direct_only: bool = False,
    max_price: Optional[int] = None,
) -> dict:
    """Search for flights using SerpApi Google Flights.

    Args:
        origin: IATA airport code (e.g., "SFO")
        destination: IATA airport code (e.g., "NRT")
        departure_date: Format YYYY-MM-DD
        return_date: Format YYYY-MM-DD, omit for one-way
        adults: Number of passengers
        direct_only: If True, only return non-stop flights
        max_price: Maximum price in USD

    Returns:
        dict with "flights" list containing price, airline, duration, stops
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        return {"error": "SERPAPI_API_KEY not configured"}

    params = {
        "engine": "google_flights",
        "departure_id": origin,
        "arrival_id": destination,
        "outbound_date": departure_date,
        "return_date": return_date,
        "adults": adults,
        "type": "1" if direct_only else "2",
        "api_key": api_key,
    }

    try:
        response = httpx.get("https://serpapi.com/search", params=params, timeout=30.0)
        response.raise_for_status()
        data = response.json()

        flights = []
        for flight in data.get("best_flights", []) + data.get("other_flights", []):
            price = flight.get("price")
            if max_price and price > max_price:
                continue
            flights.append(
                {
                    "price": price,
                    "airline": flight["flights"][0].get("airline", "Unknown"),
                    "duration": flight.get("total_duration", 0),
                    "stops": len(flight.get("flights", [])) - 1,
                    "departure": flight["flights"][0]["departure_airport"].get("time"),
                    "arrival": flight["flights"][-1]["arrival_airport"].get("time"),
                    "booking_token": flight.get("booking_token"),
                }
            )

        return {"flights": sorted(flights, key=lambda x: x["price"])[:10]}
    except Exception as e:
        return {"error": f"Failed to search flights: {str(e)}"}
