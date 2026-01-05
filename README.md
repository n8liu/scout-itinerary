# Scout

An AI travel agent built with LangGraph that searches flights, hotels, and manages calendar events.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  LangGraph State Machine                                    │
│  ┌────────┐   ┌──────────┐   ┌─────────┐   ┌────────────┐  │
│  │ Intake │──▶│ Research │──▶│ Compare │──▶│  Finalize  │  │
│  └────────┘   └────┬─────┘   └─────────┘   └────────────┘  │
│                    │ ▲                                      │
│                    ▼ │                                      │
│               ┌─────────┐                                   │
│               │  Tools  │                                   │
│               └─────────┘                                   │
├─────────────────────────────────────────────────────────────┤
│  Tools: Flights (SerpApi) │ Hotels │ Calendar │ Pinecone   │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key"
python main.py
```

## Usage

```
You: Plan a trip to Tokyo in March for 2 people. Budget $3000.
```

The agent extracts requirements, searches for options, presents comparisons, and can add events to your calendar.

## Project Structure

```
scout/
├── agent/
│   ├── graph.py      # LangGraph workflow
│   ├── nodes.py      # Intake, research, compare, finalize
│   └── state.py      # TypedDict state schema
├── tools/
│   ├── flights.py    # SerpApi Google Flights
│   ├── hotels.py     # Hotel search
│   ├── calendar.py   # Google Calendar
│   └── memory.py     # Pinecone vector store
└── config/
    └── settings.py
```

## Tech Stack

- **LangGraph** — Multi-step agentic workflow with conditional routing
- **Claude** — LLM for reasoning and tool orchestration
- **Pinecone** — Vector memory for user preferences
- **SerpApi** — Real-time flight data
- **Google Calendar API** — Trip event creation

## API Keys

| Key | Required | Purpose |
|-----|----------|---------|
| `ANTHROPIC_API_KEY` | Yes | Agent reasoning |
| `SERPAPI_API_KEY` | No | Flight search |
| `PINECONE_API_KEY` | No | Preference storage |
| `OPENAI_API_KEY` | No | Embeddings |

## Testing

```bash
pytest tests/
```

## License

MIT
