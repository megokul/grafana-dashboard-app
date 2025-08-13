import logging
import os


def setup_logging() -> None:
    """
    Configure root logging.
    Honors LOG_LEVEL env variable if present.
    """
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
