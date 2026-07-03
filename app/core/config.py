from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


class Settings:
    def __init__(self):
        self.APP_NAME = os.getenv("APP_NAME", "AgneticAI")
        self.APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
        self.DATABASE_URL = os.getenv(
            "DATABASE_URL",
            "sqlite:///./agnetic.db"
        )
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


# Create a singleton settings object
settings = Settings()