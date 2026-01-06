# Scout

An AI travel agent with a full-featured dashboard. Built with LangGraph, FastAPI, and Gemini.

## Features

- **Interactive Dashboard** — Map view of all destinations, trip management, AI chat
- **Calendar View** — Full calendar with all itinerary items, filtering by trip
- **Trip Management** — Create trips, add flights/hotels/activities, track budgets
- **AI Planning** — Chat with Scout to plan trips using natural language

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  LangGraph Agent                                            │
│  ┌────────┐   ┌──────────┐   ┌─────────┐   ┌────────────┐  │
│  │ Intake │──▶│ Research │──▶│ Compare │──▶│  Finalize  │  │
│  └────────┘   └────┬─────┘   └─────────┘   └────────────┘  │
│                    │ ▲                                      │
│                    ▼ │                                      │
│               ┌─────────┐                                   │
│               │  Tools  │                                   │
│               └─────────┘                                   │
├─────────────────────────────────────────────────────────────┤
│  FastAPI Backend + SQLite                                   │
├─────────────────────────────────────────────────────────────┤
│  Dashboard: Map (Leaflet) │ Calendar (FullCalendar) │ Chat │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
pip install -r requirements.txt
export GOOGLE_API_KEY="your-gemini-key"

# Run the dashboard
python server.py
```

Open http://localhost:8000

## CLI Mode

```bash
python main.py
```

## Project Structure

```
scout/
├── agent/           # LangGraph workflow
├── tools/           # Flight, hotel, calendar, memory tools
├── api/             # FastAPI routes and models
└── config/          # Settings
static/              # Dashboard frontend
server.py            # FastAPI server
main.py              # CLI entry point
```

## Tech Stack

- **LangGraph** — Agentic workflow with conditional routing
- **Gemini** — LLM for reasoning and tool orchestration
- **FastAPI** — REST API backend
- **Leaflet** — Interactive maps
- **FullCalendar** — Calendar views
- **Tailwind CSS** — Styling

## API Keys

| Key | Required | Purpose |
|-----|----------|---------|
| `GOOGLE_API_KEY` | Yes | Gemini AI |
| `SERPAPI_API_KEY` | No | Flight search |
| `PINECONE_API_KEY` | No | Preference storage |

## License

MIT
