# Quick Start Guide

Get Scout up and running in 5 minutes.

## Prerequisites

- Python 3.9 or higher
- pip package manager
- An Anthropic API key

## Setup Steps

### 1. Install Dependencies

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Anthropic API key
# ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Get your API key from: https://console.anthropic.com

### 3. Run Setup

```bash
python setup.py
```

This will verify your configuration and show which features are available.

### 4. Run Scout

```bash
python main.py
```

## Example Session

```
You: Plan a weekend trip to San Francisco in March for 2 people

Scout: I'd be happy to help you plan a weekend trip to San Francisco!
       To find the best options, I need a few more details:

       1. What dates in March are you considering?
       2. What's your budget for the trip?
       3. Where will you be flying from?
       4. Any preferences for flights or hotels?

You: March 15-17, budget $2000, flying from LAX, prefer direct flights

Scout: [Searches flights and hotels, presents options]
```

## Features Available by API

| Feature | API Required | Fallback |
|---------|-------------|----------|
| Core agent | ANTHROPIC_API_KEY | None (required) |
| Flight search | SERPAPI_API_KEY | Error message |
| Hotel search | SKYSCANNER_API_KEY | Mock data |
| Calendar events | Google credentials | Error message |
| Preference storage | PINECONE_API_KEY + OPENAI_API_KEY | Error message |

## Testing

```bash
# Run basic tests
pytest tests/ -v
```

## Next Steps

1. **Add more API keys**: Enable flight search, calendar integration
2. **Try examples**: Run `python example.py`
3. **Customize tools**: Edit files in `scout/tools/`
4. **Modify workflow**: Update `scout/agent/graph.py`

## Troubleshooting

### "Missing required configuration: ANTHROPIC_API_KEY"
- Add your API key to `.env` file
- Make sure `.env` is in the project root
- Restart your terminal/IDE after editing `.env`

### "ModuleNotFoundError: No module named 'langchain'"
- Activate your virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

### Rate limits or API errors
- Check your API key is valid
- Verify you have credits/quota
- Some features use mock data if APIs aren't configured

## Project Structure

```
scout-itinerary/
├── scout/              # Main package
│   ├── agent/         # LangGraph workflow
│   ├── tools/         # API integrations
│   └── config/        # Settings
├── tests/             # Test suite
├── main.py            # CLI entry point
├── example.py         # Usage examples
└── setup.py           # Setup wizard
```

## Learning Path

1. Read [README.md](README.md) for full documentation
2. Explore [scout/agent/graph.py](scout/agent/graph.py) to understand the workflow
3. Check [scout/tools/](scout/tools/) to see how tools work
4. Try modifying [scout/agent/nodes.py](scout/agent/nodes.py) to customize behavior

## Getting Help

- Check the [README.md](README.md) for detailed docs
- Review example usage in [example.py](example.py)
- Run `python setup.py` to diagnose configuration issues

Happy traveling with Scout!
