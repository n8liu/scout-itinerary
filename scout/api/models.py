"""Database models for Scout dashboard."""
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../../data/scout.db")


def get_db():
    """Get database connection."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            destination TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            budget REAL,
            travelers INTEGER DEFAULT 1,
            status TEXT DEFAULT 'planning',
            lat REAL,
            lng REAL,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS itinerary_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            item_type TEXT NOT NULL,
            start_datetime TEXT NOT NULL,
            end_datetime TEXT,
            location TEXT,
            lat REAL,
            lng REAL,
            cost REAL,
            booking_ref TEXT,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
        );
        
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
        );
    """)
    conn.commit()
    conn.close()


# Pydantic models
class TripCreate(BaseModel):
    name: str
    destination: str
    start_date: str
    end_date: str
    budget: Optional[float] = None
    travelers: int = 1
    lat: Optional[float] = None
    lng: Optional[float] = None
    notes: Optional[str] = None


class TripUpdate(BaseModel):
    name: Optional[str] = None
    destination: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    budget: Optional[float] = None
    travelers: Optional[int] = None
    status: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    notes: Optional[str] = None


class Trip(BaseModel):
    id: int
    name: str
    destination: str
    start_date: str
    end_date: str
    budget: Optional[float]
    travelers: int
    status: str
    lat: Optional[float]
    lng: Optional[float]
    notes: Optional[str]
    created_at: str
    updated_at: str


class ItineraryItemCreate(BaseModel):
    trip_id: int
    title: str
    description: Optional[str] = None
    item_type: str  # flight, hotel, activity, dining, transport
    start_datetime: str
    end_datetime: Optional[str] = None
    location: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    cost: Optional[float] = None
    booking_ref: Optional[str] = None
    notes: Optional[str] = None


class ItineraryItem(BaseModel):
    id: int
    trip_id: int
    title: str
    description: Optional[str]
    item_type: str
    start_datetime: str
    end_datetime: Optional[str]
    location: Optional[str]
    lat: Optional[float]
    lng: Optional[float]
    cost: Optional[float]
    booking_ref: Optional[str]
    notes: Optional[str]
    created_at: str


class ChatMessage(BaseModel):
    role: str
    content: str
    trip_id: Optional[int] = None


# Initialize DB on import
init_db()
