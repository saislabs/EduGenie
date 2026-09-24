import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)


class Settings:
    BASE_DIR: Path = BASE_DIR
    ENV_PATH: Path = ENV_PATH

    APP_NAME: str = os.getenv("APP_NAME", "EduGenie")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Gemini API Key & Model
    GEMINI_API_KEY: str = (
        os.getenv("GEMINI_API_KEY", "").strip()
        or os.getenv("GOOGLE_API_KEY", "").strip()
    )
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

    # Database
    DATABASE_PATH: Path = BASE_DIR / "edugenie.db"
    DATABASE_URL: str = f"sqlite:///{DATABASE_PATH}"

    # Request constraints
    MAX_INPUT_LENGTH: int = 15000
    MAX_QUESTION_LENGTH: int = 2000
    MAX_CONCEPT_LENGTH: int = 200
    MAX_SUMMARY_INPUT_LENGTH: int = 25000

    @classmethod
    def reload(cls):
        """Reload configuration from disk."""
        load_dotenv(dotenv_path=ENV_PATH, override=True)
        cls.GEMINI_API_KEY = (
            os.getenv("GEMINI_API_KEY", "").strip()
            or os.getenv("GOOGLE_API_KEY", "").strip()
        )
        cls.GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

    @classmethod
    def is_gemini_configured(cls) -> bool:
        """Check if a non-placeholder Gemini API key is configured."""
        key = cls.GEMINI_API_KEY
        if not key:
            return False
        if key in ("your_gemini_api_key_here", "your_key_here", "REPLACE_ME"):
            return False
        return len(key) > 10


settings = Settings()
