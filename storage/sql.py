from contextlib import contextmanager
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'devcontext.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

def init_db() -> sqlite3.Connection:
    """Initialize the SQLite database if it doesn't already exist."""
    db_path = os.path.realpath(DB_PATH)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    try:
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        if tables:
            return conn

        with open(SCHEMA_PATH, 'r') as f:
            schema = f.read()
        conn.executescript(schema)
        conn.commit()
    finally:
        conn.close()

    return conn


@contextmanager
def get_connection():
    """Context manager for SQLite database connection."""
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    conn = init_db()
    print(f"Database ready at {DB_PATH}")
    conn.close()

