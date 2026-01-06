# Scout: Agentic Travel Concierge

An AI-powered travel planning agent built with LangGraph that autonomously searches flights, hotels, and manages calendar events through real API integrations.

## Overview

Scout is a multi-step agentic workflow that demonstrates:
- **Tool Use Orchestration**: Coordinated calling of multiple APIs (flights, hotels, calendar)
- **State Management**: Complex state tracking through LangGraph TypedDict
- **Autonomous Decision Making**: Agent-driven workflow with conditional routing
- **Vector Memory**: Personalized recommendations through stored user preferences

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Scout Agent                             │
├─────────────────────────────────────────────────────────────────┤
│  LangGraph State Machine                                        │
│  ┌─────────┐    ┌──────────┐    ┌─────────┐    ┌────────────┐  │
│  │ Intake  │───▶│ Research │───▶│ Compare │───▶│  Finalize  │  │
│  └─────────┘    └──────────┘    └─────────┘    └────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  Tool Layer                                                     │
│  ┌──────────┐ ┌───────────┐ ┌──────────┐ ┌─────────────────┐   │
│  │ Flights  │ │  Hotels   │ │ Calendar │ │ Vector Memory   │   │
│  │ (SerpApi)│ │(Skyscanner)│ │ (Google) │ │ (Pinecone)      │   │
│  └──────────┘ └───────────┘ └──────────┘ └─────────────────────┘
└─────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
scout-itinerary/
├── scout/
│   ├── agent/
│   │   ├── graph.py          # LangGraph state machine
│   │   ├── nodes.py          # Node functions (intake, research, compare, finalize)
│   │   └── state.py          # TypedDict state schema
│   ├── tools/
│   │   ├── flights.py        # Flight search tool (SerpApi)
│   │   ├── hotels.py         # Hotel availability tool
│   │   ├── calendar.py       # Google Calendar integration
│   │   └── memory.py         # Vector store for preferences (Pinecone)
│   └── config/
│       └── settings.py       # API keys, model config
├── tests/
│   ├── test_tools.py         # Tool tests
│   └── test_agent.py         # Agent workflow tests
├── main.py                   # Entry point (CLI)
├── setup.py                  # Setup script
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd scout-itinerary

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Run setup script
python setup.py

# Edit .env file with your API keys
# At minimum, you need ANTHROPIC_API_KEY
```

Required API Keys:
- **ANTHROPIC_API_KEY** (required): Get from [console.anthropic.com](https://console.anthropic.com)

Optional API Keys (for full functionality):
- **SERPAPI_API_KEY**: Flight search via [serpapi.com](https://serpapi.com)
- **SKYSCANNER_API_KEY**: Hotel search via [partners.skyscanner.net](https://partners.skyscanner.net)
- **PINECONE_API_KEY**: Preference storage via [pinecone.io](https://pinecone.io)
- **OPENAI_API_KEY**: Embeddings for vector search via [platform.openai.com](https://platform.openai.com)

### 3. Run Scout

```bash
# Interactive CLI
python main.py

# Example usage
You: Plan a week-long trip to Tokyo in March for 2 people. Budget is $3000 total.
     We prefer direct flights and 4-star hotels.
```

## Features

### 1. Intelligent Trip Planning
- Extracts requirements from natural language
- Asks clarifying questions when needed
- Considers budget constraints

### 2. Multi-Source Search
- **Flights**: Real-time pricing via Google Flights (SerpApi)
- **Hotels**: Availability and rates (with mock data fallback)
- Filters by preferences (direct flights, star rating, price)

### 3. Personalization
- Stores user preferences in vector database
- Recalls relevant preferences for future trips
- Learns from booking patterns

### 4. Calendar Integration
- Creates trip events in Google Calendar
- Includes flight and hotel details
- Provides shareable links

## Workflow Stages

1. **Intake**: Extract travel requirements
   - Destination, dates, budget, travelers
   - Preferences (airline, hotel class, etc.)

2. **Research**: Search for options
   - Call flight and hotel APIs
   - Recall stored preferences
   - Filter by budget and requirements

3. **Compare**: Present options
   - Format results clearly
   - Provide recommendations
   - Ask for user selection

4. **Finalize**: Confirm booking
   - Create calendar event
   - Store new preferences
   - Provide next steps

## Key Technical Concepts

### LangGraph State Management

```python
class TravelState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    destination: str
    dates: dict
    budget: dict
    # ... more fields
```

State flows through nodes, with each node updating relevant fields.

### Tool Calling

Tools are defined with the `@tool` decorator:

```python
@tool
def search_flights(origin: str, destination: str, ...) -> dict:
    """Search for flights using SerpApi Google Flights."""
    # Implementation
```

The agent decides when to call tools based on the conversation context.

### Conditional Routing

```python
def should_use_tools(state: TravelState) -> str:
    """Route to tools if model requested tool calls."""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "compare"
```

### Vector Memory

User preferences are stored as embeddings for semantic search:

```python
@tool
def store_preference(user_id: str, preference_type: str, value: str):
    """Store in Pinecone for later recall."""
```

## Testing

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_tools.py -v

# Run with coverage
pytest --cov=scout tests/
```

## API Setup Guides

### Google Calendar Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable Google Calendar API
4. Create OAuth 2.0 credentials
5. Download credentials as `credentials.json`
6. First run will prompt for authentication

### Pinecone Setup

1. Sign up at [pinecone.io](https://pinecone.io)
2. Create a new index:
   - Name: `scout-preferences`
   - Dimensions: `1536` (for OpenAI embeddings)
   - Metric: `cosine`
3. Copy API key to `.env`

## Extending Scout

### Add New Tools

1. Create tool in `scout/tools/`:
```python
@tool
def my_new_tool(param: str) -> dict:
    """Tool description."""
    # Implementation
```

2. Add to `scout/tools/__init__.py`
3. Include in `graph.py` tools list
4. Agent will automatically use it when relevant

### Modify Workflow

Edit `scout/agent/graph.py` to:
- Add new nodes
- Change routing logic
- Add conditional edges

### Alternative APIs

| Feature | Current | Alternatives |
|---------|---------|-------------|
| Flights | SerpApi | Amadeus, Travelport, Duffel |
| Hotels | Skyscanner | Booking.com, Amadeus, Hotels.com |
| LLM | Anthropic Claude | OpenAI, Google Gemini |
| Vector DB | Pinecone | Weaviate, Chroma, Qdrant |

## Troubleshooting

### Missing API Keys
```
Error: Missing required configuration: ANTHROPIC_API_KEY
```
Solution: Run `python setup.py` and add keys to `.env`

### Import Errors
```
ModuleNotFoundError: No module named 'langchain'
```
Solution: `pip install -r requirements.txt`

### Google Calendar Authentication
```
Error: Google Calendar authentication required
```
Solution: Ensure `credentials.json` exists and run the app to complete OAuth flow

## Performance Considerations

- First run may be slower due to API calls
- Vector search requires OpenAI embeddings (costs apply)
- SerpApi has rate limits on free tier
- Consider caching flight/hotel results

## Security Notes

- Never commit `.env` or `credentials.json`
- API keys should have minimal required permissions
- Use environment-specific keys (dev/prod)
- Rotate keys regularly

## License

MIT

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## Resume Highlights

This project demonstrates:
- **Agentic AI**: Multi-step autonomous workflows with LangGraph
- **Tool Orchestration**: Coordinated API calls with structured outputs
- **State Management**: Complex state handling with TypedDict and reducers
- **Vector Memory**: Semantic search for personalization
- **Production Patterns**: Error handling, configuration management, testing
- **Real Integrations**: SerpApi, Google Calendar, Pinecone

Perfect for showcasing modern AI engineering skills!
