"""Entry point for Scout travel agent."""
from scout.agent.graph import agent
from scout.agent.state import TravelState
from scout.config.settings import settings
from langchain_core.messages import HumanMessage


def run_scout(user_input: str, user_id: str = "default") -> str:
    """Run the Scout travel agent.

    Args:
        user_input: User's travel request
        user_id: Unique identifier for the user (for preference storage)

    Returns:
        The agent's final response as a string
    """
    # Validate configuration
    missing = settings.validate()
    if missing:
        return f"Error: Missing required configuration: {', '.join(missing)}\n\nPlease set these environment variables in your .env file."

    # Create initial state
    initial_state: TravelState = {
        "messages": [HumanMessage(content=user_input)],
        "destination": "",
        "dates": {},
        "budget": {},
        "travelers": 1,
        "preferences": {},
        "flight_options": [],
        "hotel_options": [],
        "selected_flights": {},
        "selected_hotel": {},
        "calendar_event_id": "",
        "stage": "intake",
    }

    # Run the agent
    try:
        result = agent.invoke(initial_state)
        final_message = result["messages"][-1]

        # Extract content from the final message
        if hasattr(final_message, "content"):
            return final_message.content
        return str(final_message)

    except Exception as e:
        return f"Error running agent: {str(e)}"


def main():
    """Interactive CLI for Scout travel agent."""
    print("=" * 60)
    print("Scout: Agentic Travel Concierge")
    print("=" * 60)
    print("\nWelcome! I can help you plan your next trip.")
    print("I'll search for flights, hotels, and add events to your calendar.")
    print("\nType 'quit' or 'exit' to end the session.\n")

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if user_input.lower() in ["quit", "exit", "q"]:
                print("\nThank you for using Scout. Safe travels!")
                break

            if not user_input:
                continue

            print("\nScout: ", end="")
            response = run_scout(user_input)
            print(response)

        except KeyboardInterrupt:
            print("\n\nThank you for using Scout. Safe travels!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again.")


if __name__ == "__main__":
    main()
