import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    def __init__(self):
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
        self.ANTIGRAVITY_API_KEY = os.getenv("ANTIGRAVITY_API_KEY", "")
        self.GOOGLE_ANTIGRAVITY_API_KEY = os.getenv("GOOGLE_ANTIGRAVITY_API_KEY", "")
        self.APP_NAME = os.getenv("APP_NAME", "Sentience Layer")
        self.DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
        self.HOST = os.getenv("HOST", "0.0.0.0")
        self.PORT = int(os.getenv("PORT", "8000"))
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
