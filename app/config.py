from pathlib import Path
import os

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


class Settings:
    APP_NAME: str = os.getenv(
        "APP_NAME",
        "Customer Complaint Intelligence"
    )

    # Groq configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    GROQ_MODEL: str = os.getenv(
        "GROQ_MODEL",
        "llama-3.3-70b-versatile"
    )

    TEMPERATURE: float = float(
        os.getenv("TEMPERATURE", "0.2")
    )

    MAX_TOKENS: int = int(
        os.getenv("MAX_TOKENS", "1500")
    )

    PROMPTS_DIR: Path = BASE_DIR / "prompts"


settings = Settings()