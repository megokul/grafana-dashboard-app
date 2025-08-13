import time
import signal
import logging
from datetime import datetime

from .config import load_settings
from .logging import setup_logging
from . import db
from .generator import build_rows
from .rules import run_rules

shutdown = False


def _sig_handler(signum, frame):
    global shutdown
    shutdown = True
    logging.getLogger("main").info("Received signal %s — shutting down...", signum)


def main():
    setup_logging()
    log = logging.getLogger("main")
    cfg = load_settings()

    signal.signal(signal.SIGINT, _sig_handler)
    signal.signal(signal.SIGTERM, _sig_handler)

    conn = db.connect(cfg)
    try:
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

    except Exception as e:
        log.exception("Fatal error: %s", e)

    finally:
        try:
            conn.close()
            log.info("Database connection closed.")
        except Exception:
            pass


if __name__ == "__main__":
    main()
