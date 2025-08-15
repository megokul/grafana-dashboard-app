from dataclasses import dataclass
from dotenv import load_dotenv
import os
from typing import Optional


@dataclass(frozen=True)
class Settings:
    """
    Centralized configuration for the data generator.

    Supports both DB_* and PG_* environment variable prefixes so the same .env
    can be shared with Grafana (which commonly uses PG_*).
    """
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str
    sslmode: Optional[str] = None  # e.g., "require" for AWS RDS
    batch_size: int = 10           # rows per cycle
    sleep_seconds: int = 15        # pause between cycles (seconds)


def _require_env_any(*keys: str) -> str:
    """
    Return the first non-empty environment variable among `keys`,
    otherwise raise an EnvironmentError.
    """
    for key in keys:
        val = os.getenv(key)
        if val not in (None, ""):
            return val
    joined = ", ".join(keys)
    raise EnvironmentError(
        f"Missing required environment variable (any of): {joined}"
    )


def load_settings() -> Settings:
    """
    Load configuration from .env and process environment variables.
    Accepts either DB_* or PG_* names for compatibility with Grafana configs.
    """
    load_dotenv()

    host = _require_env_any("DB_HOST", "PG_HOST")
    port = int(_require_env_any("DB_PORT", "PG_PORT"))
    name = _require_env_any("DB_NAME", "PG_DB")
    user = _require_env_any("DB_USER", "PG_USER")
    password = _require_env_any("DB_PASSWORD", "PG_PASSWORD")

    # Optional values
    sslmode = os.getenv("DB_SSLMODE") or os.getenv("PG_SSLMODE")
    batch_size = int(os.getenv("BATCH_SIZE", "10"))
    sleep_seconds = int(os.getenv("SLEEP_SECONDS", "15"))

    return Settings(
        db_host=host,
        db_port=port,
        db_name=name,
        db_user=user,
        db_password=password,
        sslmode=sslmode,
        batch_size=batch_size,
        sleep_seconds=sleep_seconds,
    )
