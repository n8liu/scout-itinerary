"""Google Calendar integration tool."""
from langchain_core.tools import tool
import os


@tool
def create_trip_event(
    title: str,
    start_date: str,
    end_date: str,
    description: str,
    location: str,
) -> dict:
    """Create a calendar event for the trip.

    Args:
        title: Event title (e.g., "Tokyo Trip")
        start_date: Format YYYY-MM-DD
        end_date: Format YYYY-MM-DD
        description: Trip details including flight/hotel info
        location: Destination city

    Returns:
        dict with "event_id" and "link" to calendar event
    """
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        from google.auth.transport.requests import Request
        from google_auth_oauthlib.flow import InstalledAppFlow

        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        creds = None

        # Check if we have stored credentials
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        # If there are no (valid) credentials available, return instructions
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                return {
                    "error": "Google Calendar authentication required. Run setup first.",
                    "instructions": "Please authenticate with Google Calendar",
                }

        service = build("calendar", "v3", credentials=creds)

        event = {
            "summary": title,
            "location": location,
            "description": description,
            "start": {"date": start_date},
            "end": {"date": end_date},
        }

        result = service.events().insert(calendarId="primary", body=event).execute()
        return {"event_id": result["id"], "link": result.get("htmlLink", "")}

    except ImportError:
        return {
            "error": "Google Calendar libraries not installed",
            "instructions": "Install with: pip install google-api-python-client google-auth-oauthlib",
        }
    except Exception as e:
        return {"error": f"Failed to create calendar event: {str(e)}"}
