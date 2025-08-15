from typing import Iterable, Tuple, List
from pathlib import Path
import logging

import psycopg2
from psycopg2.extensions import connection as PGConnection
from psycopg2.extras import execute_batch

from .config import Settings

log = logging.getLogger("db")


def _sql_dir_candidates() -> List[Path]:
    """
    Return plausible locations of the sql/ directory.

    Layouts we support:
      - Container layout:
          /app/app/*.py   (this file)
          /app/sql/*.sql  (SQL files)
      - Project-root execution:
          <repo>/data_generator/app/*.py
          <repo>/sql/*.sql
      - CWD fallback:
          $PWD/sql/*.sql
    """
    here = Path(__file__).resolve()
    return [
        here.parent.parent / "sql",        # /app/sql  (container case)
        here.parent.parent.parent / "sql", # <repo>/sql (if run from repo root)
        Path.cwd() / "sql",                # CWD fallback
    ]


def _load_sql(filename: str) -> str:
    """
    Load an SQL file from one of the candidate sql/ directories.
    Logs the resolved path when found.
    """
    for base in _sql_dir_candidates():
        path = base / filename
        if path.exists():
            log.info("Loading SQL from %s", path)
            return path.read_text(encoding="utf-8")

    searched = ", ".join(str(p / filename) for p in _sql_dir_candidates())
    raise FileNotFoundError(f"SQL file {filename} not found. Searched: {searched}")


CREATE_TABLE_SQL = _load_sql("schema.sql")
INSERT_SQL = _load_sql("insert.sql")


def connect(cfg: Settings) -> PGConnection:
    """
    Establish and return a PostgreSQL connection.
    Adds sslmode if provided (e.g., 'require' for AWS RDS).
    """
    log.info(
        "Connecting to PostgreSQL at %s:%s (db=%s, user=%s, sslmode=%s)",
        cfg.db_host,
        cfg.db_port,
        cfg.db_name,
        cfg.db_user,
        cfg.sslmode or "default",
    )

    kwargs = dict(
        host=cfg.db_host,
        port=cfg.db_port,
        dbname=cfg.db_name,
        user=cfg.db_user,
        password=cfg.db_password,
    )
    if cfg.sslmode:
        kwargs["sslmode"] = cfg.sslmode

    conn = psycopg2.connect(**kwargs)
    conn.autocommit = False
    return conn


def ensure_schema(conn: PGConnection) -> None:
    """
    Ensure the target table(s) exist.
    """
    log.info("Ensuring database schema...")
    with conn.cursor() as cur:
        cur.execute(CREATE_TABLE_SQL)
    conn.commit()
    log.info("Schema ready.")


def insert_batch(conn: PGConnection, rows: Iterable[Tuple]) -> int:
    """
    Insert a batch of rows using psycopg2.execute_batch.
    Returns number of rows inserted.
    """
    rows = list(rows)
    if not rows:
        return 0

    with conn.cursor() as cur:
        execute_batch(cur, INSERT_SQL, rows, page_size=100)

    log.info("Inserted %d rows.", len(rows))
    return len(rows)
