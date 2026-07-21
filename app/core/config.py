from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()


class Settings:
    def __init__(self):

        self.APP_NAME = os.getenv(
            "APP_NAME",
            "AgneticAI"
        )

        self.APP_VERSION = os.getenv(
            "APP_VERSION",
            "0.1.0"
        )

        self.ENVIRONMENT = os.getenv(
            "ENVIRONMENT",
            "development"
        )

        self.DATABASE_URL = os.getenv(
            "DATABASE_URL",
            "sqlite:///./aisdr.db"
        )

        self.GEMINI_API_KEY = os.getenv(
            "GEMINI_API_KEY",
            ""
        )

        self.TAVILY_API_KEY = os.getenv(
            "TAVILY_API_KEY",
            ""
        )

        self.AI_MODEL = os.getenv(
            "AI_MODEL",
            "gemini-2.5-flash"
        )

        self.RESEARCH_CACHE_DAYS = int(
            os.getenv(
                "RESEARCH_CACHE_DAYS",
                "7"
            )
        )

        self.DISCOVERY_PROVIDER = os.getenv(
            "DISCOVERY_PROVIDER",
            "mock"
        )

        self.AI_TEMPERATURE = float(
            os.getenv("AI_TEMPERATURE", "0.2")
        )

        self.AI_MAX_RETRIES = int(
            os.getenv("AI_MAX_RETRIES", "3")
        )

        self.AI_TIMEOUT = int(
            os.getenv("AI_TIMEOUT", "60")
        )

        self.LLM_PROVIDER = os.getenv(
            "LLM_PROVIDER",
            "gemini",
        )
        
        # ==========================================================
        # Email Provider
        # ==========================================================

        self.EMAIL_PROVIDER = os.getenv(
            "EMAIL_PROVIDER",
            "gmail",
        )


        # ==========================================================
        # Google OAuth
        # ==========================================================

        self.GOOGLE_CLIENT_ID = os.getenv(
            "GOOGLE_CLIENT_ID",
            "",
        )

        self.GOOGLE_CLIENT_SECRET = os.getenv(
            "GOOGLE_CLIENT_SECRET",
            "",
        )

        self.GOOGLE_REDIRECT_URI = os.getenv(
            "GOOGLE_REDIRECT_URI",
            "http://localhost",
        )

        self.GOOGLE_CREDENTIALS_FILE = os.getenv(
            "GOOGLE_CREDENTIALS_FILE",
            "credentials.json",
        )

        self.GOOGLE_TOKEN_FILE = os.getenv(
            "GOOGLE_TOKEN_FILE",
            "token.json",
        )

        self.GOOGLE_SCOPES = [
            "https://www.googleapis.com/auth/gmail.send",
        ]


# Create a singleton settings object
settings = Settings()