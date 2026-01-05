# Scout Architecture Documentation

## System Overview

Scout is a LangGraph-based agentic AI system that autonomously orchestrates travel planning through a multi-stage workflow.

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        User Interface (CLI)                       │
│                          main.py                                  │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                    LangGraph Agent (graph.py)                     │
│                                                                   │
│  ┌────────────┐     ┌────────────┐     ┌────────────┐            │
│  │   Intake   │────▶│  Research  │────▶│  Compare   │            │
│  │   Node     │     │    Node    │     │    Node    │            │
│  └────────────┘     └──────┬─────┘     └────────────┘            │
│                            │ ▲                │                   │
│                            ▼ │                ▼                   │
│                      ┌─────────────┐    ┌────────────┐            │
│                      │    Tools    │    │  Finalize  │            │
│                      │    Node     │    │    Node    │            │
│                      └─────────────┘    └────────────┘            │
│                            │                                      │
└────────────────────────────┼──────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                         Tool Layer                                │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │   Flights    │  │    Hotels    │  │   Calendar   │            │
│  │  (SerpApi)   │  │ (Skyscanner) │  │   (Google)   │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
│                                                                   │
│  ┌──────────────────────────────────────────────────┐            │
│  │           Vector Memory (Pinecone)               │            │
│  │         store_preference / recall_preferences    │            │
│  └──────────────────────────────────────────────────┘            │
└──────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                      External APIs                                │
│                                                                   │
│  SerpApi │ Skyscanner │ Google Calendar │ Pinecone │ OpenAI      │
└──────────────────────────────────────────────────────────────────┘
```

## Workflow State Machine

```
START
  │
  ▼
┌─────────────────────┐
│   INTAKE NODE       │  Extract requirements from user
│                     │  - Destination
│  Input: User query  │  - Dates
│  Output: State with │  - Budget
│          extracted  │  - Preferences
│          info       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  RESEARCH NODE      │  Search for options
│                     │
│  Actions:           │
│  1. Recall prefs    │──┐
│  2. Search flights  │  │ Tool calls?
│  3. Search hotels   │  │
└──────────┬──────────┘  │
           │              │
           │              ▼
           │         ┌─────────────────────┐
           │         │    TOOLS NODE       │
           │         │                     │
           │         │  Execute tool calls │
           │         │  Return results     │
           │         └──────────┬──────────┘
           │                    │
           │◀───────────────────┘
           │ (Loop until done)
           │
           ▼
┌─────────────────────┐
│   COMPARE NODE      │  Present options
│                     │
│  Actions:           │  - Format results
│  - Show flights     │  - Make recommendations
│  - Show hotels      │  - Ask for selection
│  - Recommend best   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  FINALIZE NODE      │  Confirm booking
│                     │
│  Actions:           │  - Create calendar event
│  1. Summarize       │  - Store preferences
│  2. Create event    │  - Provide next steps
│  3. Store prefs     │
└──────────┬──────────┘
           │
           ▼
          END
```

## Data Flow

### 1. Initial Request

```
User Input: "Plan a trip to Tokyo in March for 2 people, budget $3000"
           │
           ▼
    Intake Node
           │
           ▼
State Updated:
{
  "destination": "Tokyo",
  "dates": {"start": "2025-03-15", "end": "2025-03-22"},
  "budget": {"total": 3000},
  "travelers": 2,
  "preferences": {},
  "stage": "research"
}
```

### 2. Research Phase

```
Research Node
     │
     ├──▶ recall_preferences(user_id="alice", query="Tokyo trip")
     │         │
     │         ▼
     │    Returns: ["Prefers direct flights", "Likes 4-star hotels"]
     │
     ├──▶ search_flights(origin="SFO", destination="NRT", ...)
     │         │
     │         ▼
     │    Returns: [
     │      {price: 850, airline: "United", stops: 0},
     │      {price: 650, airline: "ANA", stops: 1},
     │      ...
     │    ]
     │
     └──▶ search_hotels(destination="Tokyo", checkin="2025-03-15", ...)
           │
           ▼
      Returns: [
        {name: "Tokyo Hotel", price: 200, stars: 4},
        ...
      ]
```

### 3. State Evolution

```
Initial State                Research Complete           Finalized
┌──────────────┐            ┌──────────────┐            ┌──────────────┐
│ messages: [] │            │ messages: [] │            │ messages: [] │
│ destination: │            │ destination: │            │ destination: │
│   ""         │  ────▶     │   "Tokyo"    │  ────▶     │   "Tokyo"    │
│ flight_opts: │            │ flight_opts: │            │ selected_flt:│
│   []         │            │   [...]      │            │   {...}      │
│ stage:       │            │ stage:       │            │ stage:       │
│   "intake"   │            │   "compare"  │            │   "complete" │
└──────────────┘            └──────────────┘            └──────────────┘
```

## Component Details

### State Schema (state.py)

```python
TravelState = TypedDict with:
  - messages: List[BaseMessage]     # Conversation history
  - destination: str                # Where to go
  - dates: dict                     # When to go
  - budget: dict                    # How much to spend
  - travelers: int                  # How many people
  - preferences: dict               # User preferences
  - flight_options: list            # Search results
  - hotel_options: list             # Search results
  - selected_flights: dict          # User choice
  - selected_hotel: dict            # User choice
  - calendar_event_id: str          # Created event
  - stage: str                      # Current workflow stage
```

### Conditional Routing (graph.py)

```python
def should_use_tools(state: TravelState) -> str:
    """
    Decision logic:

    If last message has tool_calls:
        ────▶ "tools"  (execute tools)
    Else:
        ────▶ "compare" (proceed to comparison)
    """
```

This creates a loop:
```
Research ──[has tool calls]──▶ Tools ──▶ Research
    │
    └──[no tool calls]──▶ Compare
```

### Tool Execution Flow

```
1. Agent (in Research Node):
   "I need to search for flights from SFO to NRT"

2. LLM generates tool call:
   {
     "name": "search_flights",
     "arguments": {
       "origin": "SFO",
       "destination": "NRT",
       "departure_date": "2025-03-15",
       "return_date": "2025-03-22",
       "adults": 2
     }
   }

3. Routing function:
   should_use_tools() ──▶ "tools"

4. Tools Node:
   - Executes search_flights()
   - Calls SerpApi
   - Returns flight data

5. Back to Research Node:
   - Receives flight results
   - Decides if more tools needed
   - Or proceeds to Compare
```

## Message Flow

```
User Message
    │
    ▼
┌───────────────────────────────────────┐
│ LLM (with tools bound)                │
│                                       │
│ System: "You are a travel agent..."  │
│ User: "Plan a trip to Tokyo"         │
│                                       │
│ LLM reasons about:                    │
│ - What info is needed?                │
│ - What tools to call?                 │
│ - What to ask user?                   │
└───────────────┬───────────────────────┘
                │
                ├──▶ Regular response (text)
                │
                └──▶ Tool call request
                        │
                        ▼
                   Tools Node
                        │
                        ▼
                   Tool results
                        │
                        ▼
                Back to LLM (with results)
```

## Error Handling Strategy

```
┌─────────────────┐
│ Tool Called     │
└────────┬────────┘
         │
         ▼
    API Key exists?
         │
    ┌────┴────┐
    │         │
   Yes       No
    │         │
    ▼         ▼
Make API  Return error
  call     + fallback
    │
    ├──▶ Success ──▶ Return data
    │
    └──▶ Failure ──▶ Return error message
```

Each tool implements:
1. API key validation
2. Try/except for API calls
3. Meaningful error messages
4. Fallback behavior (where applicable)

## Scalability Considerations

### Current Architecture
- Synchronous execution
- In-memory state
- CLI interface
- Single user

### Production Scaling Path

```
Current (CLI)
    │
    ▼
Add persistence
    │ (SQLite/PostgreSQL for state)
    ▼
Add web API
    │ (FastAPI/Flask)
    ▼
Add multi-user support
    │ (User sessions, auth)
    ▼
Add async execution
    │ (Background jobs, queues)
    ▼
Add distributed execution
    │ (Celery, RabbitMQ)
    ▼
Production Scale
```

## Extension Points

### 1. Add New Tools
Location: `scout/tools/new_tool.py`
```python
@tool
def new_tool(...) -> dict:
    """Your tool"""
    pass
```

### 2. Add New Nodes
Location: `scout/agent/nodes.py`
```python
def new_node(state: TravelState) -> dict:
    """Your node logic"""
    return {"messages": [...]}
```

Then update `graph.py`:
```python
workflow.add_node("new_node", new_node)
workflow.add_edge("some_node", "new_node")
```

### 3. Modify Routing
Location: `scout/agent/graph.py`
```python
def custom_router(state: TravelState) -> str:
    """Your routing logic"""
    if condition:
        return "path_a"
    return "path_b"

workflow.add_conditional_edges(
    "node_name",
    custom_router,
    {"path_a": "node_a", "path_b": "node_b"}
)
```

### 4. Add State Fields
Location: `scout/agent/state.py`
```python
class TravelState(TypedDict):
    # ... existing fields
    new_field: YourType  # Add your field
```

## Performance Characteristics

### Latency Breakdown (Typical)

```
Total Time: ~15-30 seconds

Intake Node:       2-3s   (LLM call)
Research Node:     3-5s   (LLM reasoning)
Tool Calls:        5-15s  (API latency)
  - Flights:       3-8s
  - Hotels:        2-5s
  - Preferences:   1-2s
Compare Node:      2-3s   (LLM call)
Finalize Node:     2-3s   (LLM + calendar)
```

### Token Usage (Typical)

```
Per workflow execution: ~3,000-8,000 tokens

Breakdown:
- System prompts:       ~500 tokens
- User messages:        ~200-500 tokens
- Tool definitions:     ~1,000 tokens
- Tool results:         ~1,000-3,000 tokens
- LLM responses:        ~1,000-2,000 tokens
```

## Security Considerations

1. **API Keys**
   - Stored in `.env` (not committed)
   - Validated at runtime
   - Never logged or exposed

2. **User Input**
   - LLM handles validation
   - No direct SQL/command injection vectors
   - Tools have typed parameters

3. **Tool Execution**
   - Sandboxed through LangChain
   - No arbitrary code execution
   - Explicit tool allowlist

4. **Data Privacy**
   - Preferences stored per user_id
   - No PII in logs
   - Calendar events only with consent

## Monitoring & Debugging

### LangGraph Checkpointing

Enable checkpointing for debugging:
```python
from langgraph.checkpoint.sqlite import SqliteSaver

memory = SqliteSaver.from_conn_string(":memory:")
agent = workflow.compile(checkpointer=memory)
```

### LangSmith Integration

Add tracing:
```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-key"
```

### Custom Logging

Add to nodes:
```python
def research_node(state: TravelState) -> dict:
    logger.info(f"Research stage: {state['destination']}")
    # ... rest of node
```

## Testing Strategy

### Unit Tests
- Individual tool functions
- Node functions (with mocked LLM)
- Routing logic
- State validation

### Integration Tests
- Full workflow with mocked APIs
- Tool calls with real APIs (optional)
- Error handling paths

### End-to-End Tests
- Complete user journeys
- Multi-turn conversations
- Edge cases and error scenarios

## Deployment Options

### Local Development
```bash
python main.py
```

### Docker
```dockerfile
FROM python:3.11
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

### Web API
```python
from fastapi import FastAPI
from main import run_scout

app = FastAPI()

@app.post("/plan")
async def plan_trip(request: TripRequest):
    return run_scout(request.query)
```

### Serverless
- AWS Lambda + API Gateway
- Google Cloud Functions
- Azure Functions

Each requires:
1. Containerization
2. Environment variable management
3. Timeout handling (increase limits)
4. Cold start optimization
