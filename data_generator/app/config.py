from dataclasses import dataclass
from dotenv import load_dotenv
import os


@dataclass(frozen=True)
class Settings:
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str
    batch_size: int = 10        # Rows per cycle
    sleep_seconds: int = 15     # Pause between cycles (seconds)


def _require_env(key: str) -> str:
    """
    Get an environment variable or raise an error if missing.
    """
    value = os.getenv(key)
    if value in (None, ""):
        raise EnvironmentError(f"Missing required environment variable: {key}")
    return value


def load_settings() -> Settings:
    """
    Load configuration from .env and process environment variables.
    Raises EnvironmentError if required keys are missing.
    """
    load_dotenv()
    return Settings(
        db_host=_require_env("DB_HOST"),
        db_port=int(_require_env("DB_PORT")),
        db_name=_require_env("DB_NAME"),
        db_user=_require_env("DB_USER"),
        db_password=_require_env("DB_PASSWORD"),
        batch_size=int(os.getenv("BATCH_SIZE", "10")),
        sleep_seconds=int(os.getenv("SLEEP_SECONDS", "15")),
    )
