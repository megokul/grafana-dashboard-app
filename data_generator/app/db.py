from typing import Iterable, Tuple
from pathlib import Path
import logging
import psycopg2
from psycopg2.extensions import connection as PGConnection
from .config import Settings

log = logging.getLogger("db")

# Path to SQL files (relative to project root)
BASE_DIR = Path(__file__).resolve().parent.parent  # data_generator/
SQL_DIR = BASE_DIR / "sql"

# Load SQL files
def _load_sql(filename: str) -> str:
    path = SQL_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"SQL file not found: {path}")
    return path.read_text()

CREATE_TABLE_SQL = _load_sql("schema.sql")
INSERT_SQL = _load_sql("insert.sql")


def connect(cfg: Settings) -> PGConnection:
    """
    Establish and return a PostgreSQL connection.
    """
    log.info(
        "Connecting to PostgreSQL at %s:%s (db=%s, user=%s)",
        cfg.db_host,
        cfg.db_port,
        cfg.db_name,
        cfg.db_user,
    )
    conn = psycopg2.connect(
        host=cfg.db_host,
        port=cfg.db_port,
        dbname=cfg.db_name,
        user=cfg.db_user,
        password=cfg.db_password,
    )
    conn.autocommit = False
    return conn


def ensure_schema(conn: PGConnection) -> None:
    """
    Create the banking_data table and indexes if they don't exist.
    """
    with conn, conn.cursor() as cur:
        cur.execute(CREATE_TABLE_SQL)
    log.info("Ensured schema and indexes exist.")


def insert_batch(conn: PGConnection, rows: Iterable[Tuple]) -> None:
    """
    Insert a batch of rows in one transaction.
    """
    with conn, conn.cursor() as cur:
        cur.executemany(INSERT_SQL, rows)
    log.info("Inserted %d rows.", len(rows) if hasattr(rows, "__len__") else -1)
