import time
import signal
import logging
from typing import Optional
from datetime import datetime

from .config import load_settings
from .logging import setup_logging
from . import db
from .generator import build_rows
from .rules import run_rules

shutdown = False


def _sig_handler(signum, frame):
    """
    Signal handler to trigger graceful shutdown.
    """
    global shutdown
    shutdown = True
    logging.getLogger("main").info(
        "Received signal %s — shutting down...", signum
    )


def main():
    """
    Entry point for the data generator service.
    Continuously generates synthetic transactions and inserts them into PostgreSQL.
    """
    setup_logging()
    log = logging.getLogger("main")
    cfg = load_settings()

    signal.signal(signal.SIGINT, _sig_handler)
    signal.signal(signal.SIGTERM, _sig_handler)

    conn: Optional[db.PGConnection] = None
    try:
        conn = db.connect(cfg)
        db.ensure_schema(conn)

        while not shutdown:
            ts = datetime.utcnow()
            rows = build_rows(cfg.batch_size, run_rules, ts)

            if rows:
                db.insert_batch(conn, rows)
                conn.commit()
                log.info("Batch inserted at %s", ts.isoformat())
            else:
                log.warning("No rows generated this cycle.")

            time.sleep(cfg.sleep_seconds)

    except Exception:
        log.exception("Fatal error in main loop.")
    finally:
        if conn is not None:
            try:
                conn.close()
                log.info("Database connection closed.")
            except Exception:
                log.exception("Error closing database connection.")


if __name__ == "__main__":
    main()
