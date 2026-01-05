"""Settings and configuration management."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # API Keys
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "")
    SKYSCANNER_API_KEY = os.getenv("SKYSCANNER_API_KEY", "")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # Pinecone Configuration
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "scout-preferences")

    # Google Calendar
    GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "./credentials.json")

    # Model Configuration
    MODEL_NAME = os.getenv("MODEL_NAME", "claude-sonnet-4-20250514")
    MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0"))

    @classmethod
    def validate(cls) -> list[str]:
        """Validate that required settings are present."""
        missing = []

        if not cls.ANTHROPIC_API_KEY:
            missing.append("ANTHROPIC_API_KEY")

        return missing

    @classmethod
    def is_configured(cls) -> bool:
        """Check if all required settings are configured."""
        return len(cls.validate()) == 0


settings = Settings()
