"""Example usage of Scout travel agent."""
from main import run_scout


def example_simple():
    """Simple example: Quick trip planning."""
    print("=" * 60)
    print("Example 1: Simple Trip Planning")
    print("=" * 60)

    response = run_scout(
        "I want to visit Tokyo for 5 days in April. Budget is $2500. "
        "I need direct flights from SFO and prefer 4-star hotels."
    )
    print(response)


def example_detailed():
    """Detailed example: Multi-city trip."""
    print("\n" + "=" * 60)
    print("Example 2: Multi-City Trip")
    print("=" * 60)

    response = run_scout(
        "Plan a 10-day trip to Japan visiting Tokyo and Kyoto. "
        "Traveling with my partner. Budget is $5000 total. "
        "We prefer business class flights if available and luxury hotels."
    )
    print(response)


if __name__ == "__main__":
    # Run examples
    # Note: These require ANTHROPIC_API_KEY to be set
    example_simple()
    # example_detailed()
