"""Itinerary management tools."""
from langchain_core.tools import tool
from scout.api.models import get_db, ItineraryItemCreate

@tool
def add_itinerary_item(
    trip_id: int,
    title: str,
    item_type: str,
    start_datetime: str,
    end_datetime: str = None,
    location: str = None,
    description: str = None,
    cost: float = None
) -> dict:
    """Add an item to the trip itinerary.
    
    Args:
        trip_id: ID of the trip
        title: Title of the event (e.g. "Flight to Tokyo")
        item_type: One of: flight, hotel, activity, dining, transport
        start_datetime: ISO format YYYY-MM-DDTHH:MM:SS
        end_datetime: ISO format YYYY-MM-DDTHH:MM:SS (optional)
        location: Address or place name
        description: Details
        cost: Price in USD
    """
    try:
        conn = get_db()
        cursor = conn.execute("""
            INSERT INTO itinerary_items 
            (trip_id, title, description, item_type, start_datetime, end_datetime, location, cost)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (trip_id, title, description, item_type, start_datetime, end_datetime, location, cost))
        conn.commit()
        item_id = cursor.lastrowid
        conn.close()
        return {"status": "success", "item_id": item_id, "message": f"Added {title} to itinerary"}
    except Exception as e:
        return {"error": str(e)}

@tool
def list_trips() -> dict:
    """List all available trips to get their IDs."""
    conn = get_db()
    rows = conn.execute("SELECT id, name, destination, start_date FROM trips").fetchall()
    conn.close()
    return {"trips": [dict(row) for row in rows]}
