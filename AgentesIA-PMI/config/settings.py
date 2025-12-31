import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Configuration settings for the AI Agents PMI system"""

    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "claude-3-5-sonnet-20241022")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

    @classmethod
    def validate(cls):
        """Validate that required settings are present"""
        required = {
            "ANTHROPIC_API_KEY": cls.ANTHROPIC_API_KEY,
            "NOTION_API_KEY": cls.NOTION_API_KEY,
            "NOTION_DATABASE_ID": cls.NOTION_DATABASE_ID
        }

        missing = [key for key, value in required.items() if not value]

        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

        return True

settings = Settings()
