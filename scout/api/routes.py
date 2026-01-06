"""API routes for Scout dashboard."""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from .models import (
    get_db, Trip, TripCreate, TripUpdate,
    ItineraryItem, ItineraryItemCreate, ChatMessage
)

router = APIRouter()


# Trip endpoints
@router.get("/trips", response_model=List[Trip])
def get_trips(status: Optional[str] = None):
    """Get all trips, optionally filtered by status."""
    conn = get_db()
    if status:
        rows = conn.execute(
            "SELECT * FROM trips WHERE status = ? ORDER BY start_date DESC", (status,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM trips ORDER BY start_date DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]


@router.get("/trips/{trip_id}", response_model=Trip)
def get_trip(trip_id: int):
    """Get a single trip by ID."""
    conn = get_db()
    row = conn.execute("SELECT * FROM trips WHERE id = ?", (trip_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Trip not found")
    return dict(row)


@router.post("/trips", response_model=Trip)
def create_trip(trip: TripCreate):
    """Create a new trip."""
    conn = get_db()
    cursor = conn.execute("""
        INSERT INTO trips (name, destination, start_date, end_date, budget, travelers, lat, lng, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (trip.name, trip.destination, trip.start_date, trip.end_date, 
          trip.budget, trip.travelers, trip.lat, trip.lng, trip.notes))
    conn.commit()
    row = conn.execute("SELECT * FROM trips WHERE id = ?", (cursor.lastrowid,)).fetchone()
    conn.close()
    return dict(row)


@router.put("/trips/{trip_id}", response_model=Trip)
def update_trip(trip_id: int, trip: TripUpdate):
    """Update a trip."""
    conn = get_db()
    existing = conn.execute("SELECT * FROM trips WHERE id = ?", (trip_id,)).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Trip not found")
    
    updates = {k: v for k, v in trip.model_dump().items() if v is not None}
    if updates:
        set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
        values = list(updates.values()) + [trip_id]
        conn.execute(f"UPDATE trips SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?", values)
        conn.commit()
    
    row = conn.execute("SELECT * FROM trips WHERE id = ?", (trip_id,)).fetchone()
    conn.close()
    return dict(row)


@router.delete("/trips/{trip_id}")
def delete_trip(trip_id: int):
    """Delete a trip."""
    conn = get_db()
    conn.execute("DELETE FROM trips WHERE id = ?", (trip_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted"}


# Itinerary endpoints
@router.get("/trips/{trip_id}/itinerary", response_model=List[ItineraryItem])
def get_itinerary(trip_id: int):
    """Get all itinerary items for a trip."""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM itinerary_items WHERE trip_id = ? ORDER BY start_datetime",
        (trip_id,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


@router.post("/itinerary", response_model=ItineraryItem)
def create_itinerary_item(item: ItineraryItemCreate):
    """Create a new itinerary item."""
    conn = get_db()
    cursor = conn.execute("""
        INSERT INTO itinerary_items 
        (trip_id, title, description, item_type, start_datetime, end_datetime, 
         location, lat, lng, cost, booking_ref, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (item.trip_id, item.title, item.description, item.item_type,
          item.start_datetime, item.end_datetime, item.location,
          item.lat, item.lng, item.cost, item.booking_ref, item.notes))
    conn.commit()
    row = conn.execute("SELECT * FROM itinerary_items WHERE id = ?", (cursor.lastrowid,)).fetchone()
    conn.close()
    return dict(row)


@router.delete("/itinerary/{item_id}")
def delete_itinerary_item(item_id: int):
    """Delete an itinerary item."""
    conn = get_db()
    conn.execute("DELETE FROM itinerary_items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted"}


# Calendar endpoint - returns all items formatted for calendar
@router.get("/calendar")
def get_calendar_events(start: Optional[str] = None, end: Optional[str] = None):
    """Get all events for calendar view."""
    conn = get_db()
    
    query = """
        SELECT i.*, t.name as trip_name, t.destination 
        FROM itinerary_items i
        JOIN trips t ON i.trip_id = t.id
    """
    params = []
    
    if start and end:
        query += " WHERE i.start_datetime >= ? AND i.start_datetime <= ?"
        params = [start, end]
    
    query += " ORDER BY i.start_datetime"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    
    # Format for FullCalendar
    events = []
    colors = {
        'flight': '#3b82f6',
        'hotel': '#8b5cf6',
        'activity': '#10b981',
        'dining': '#f59e0b',
        'transport': '#6366f1'
    }
    
    for row in rows:
        events.append({
            'id': row['id'],
            'title': row['title'],
            'start': row['start_datetime'],
            'end': row['end_datetime'] or row['start_datetime'],
            'color': colors.get(row['item_type'], '#6b7280'),
            'extendedProps': {
                'trip_id': row['trip_id'],
                'trip_name': row['trip_name'],
                'destination': row['destination'],
                'item_type': row['item_type'],
                'location': row['location'],
                'cost': row['cost'],
                'notes': row['notes']
            }
        })
    
    return events


# Chat endpoint
@router.post("/chat")
async def chat(message: ChatMessage):
    """Chat with Scout AI agent."""
    from main import run_scout
    
    response = run_scout(message.content)
    
    # Store messages if trip_id provided
    if message.trip_id:
        conn = get_db()
        conn.execute(
            "INSERT INTO chat_messages (trip_id, role, content) VALUES (?, ?, ?)",
            (message.trip_id, "user", message.content)
        )
        conn.execute(
            "INSERT INTO chat_messages (trip_id, role, content) VALUES (?, ?, ?)",
            (message.trip_id, "assistant", response)
        )
        conn.commit()
        conn.close()
    
    return {"response": response}


# Stats endpoint
@router.get("/stats")
def get_stats():
    """Get dashboard statistics."""
    conn = get_db()
    
    total_trips = conn.execute("SELECT COUNT(*) FROM trips").fetchone()[0]
    upcoming_trips = conn.execute(
        "SELECT COUNT(*) FROM trips WHERE start_date >= date('now') AND status != 'completed'"
    ).fetchone()[0]
    total_budget = conn.execute(
        "SELECT COALESCE(SUM(budget), 0) FROM trips WHERE status != 'cancelled'"
    ).fetchone()[0]
    total_items = conn.execute("SELECT COUNT(*) FROM itinerary_items").fetchone()[0]
    
    conn.close()
    
    return {
        "total_trips": total_trips,
        "upcoming_trips": upcoming_trips,
        "total_budget": total_budget,
        "total_items": total_items
    }
