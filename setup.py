"""Setup script for Scout travel agent."""
import os
from pathlib import Path


def setup_environment():
    """Set up environment and check configuration."""
    print("=" * 60)
    print("Scout Travel Agent - Setup")
    print("=" * 60)

    # Check if .env exists
    env_file = Path(".env")
    if not env_file.exists():
        print("\n.env file not found. Creating from .env.example...")
        example_file = Path(".env.example")
        if example_file.exists():
            env_file.write_text(example_file.read_text())
            print("✓ Created .env file")
            print("\nPlease edit .env and add your API keys:")
            print("  - ANTHROPIC_API_KEY (required)")
            print("  - SERPAPI_API_KEY (for flight search)")
            print("  - SKYSCANNER_API_KEY (for hotel search)")
            print("  - PINECONE_API_KEY (for preference storage)")
            print("  - OPENAI_API_KEY (for embeddings)")
        else:
            print("✗ .env.example not found")
    else:
        print("✓ .env file exists")

    # Check for required API keys
    from dotenv import load_dotenv

    load_dotenv()

    print("\nChecking API keys...")
    required_keys = ["ANTHROPIC_API_KEY"]
    optional_keys = [
        "SERPAPI_API_KEY",
        "SKYSCANNER_API_KEY",
        "PINECONE_API_KEY",
        "OPENAI_API_KEY",
    ]

    missing_required = []
    missing_optional = []

    for key in required_keys:
        if os.getenv(key):
            print(f"✓ {key} configured")
        else:
            print(f"✗ {key} NOT configured")
            missing_required.append(key)

    for key in optional_keys:
        if os.getenv(key):
            print(f"✓ {key} configured")
        else:
            print(f"⚠ {key} not configured (optional)")
            missing_optional.append(key)

    if missing_required:
        print(
            f"\n⚠ Warning: Missing required API keys: {', '.join(missing_required)}"
        )
        print("The agent will not work without these keys.")
        return False

    if missing_optional:
        print(f"\nNote: Some optional features will use mock data or be disabled.")

    print("\n" + "=" * 60)
    print("Setup complete!")
    print("=" * 60)
    print("\nTo run Scout:")
    print("  python main.py")
    print("\nTo run tests:")
    print("  pytest tests/")

    return True


if __name__ == "__main__":
    setup_environment()
