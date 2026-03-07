from __future__ import annotations

from pathlib import Path
import sqlite3

from PySide6.QtCore import QStandardPaths

from app.config import DEFAULT_DB_FILENAME


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS record_drafts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_key TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    camera_name TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL
);
"""


def default_db_path() -> Path:
    locations = QStandardPaths.standardLocations(QStandardPaths.StandardLocation.AppDataLocation)
    base_path = Path(locations[0]) if locations else Path.cwd() / ".packpal"
    base_path.mkdir(parents=True, exist_ok=True)
    return base_path / DEFAULT_DB_FILENAME


def connect(db_path: str | Path | None = None) -> sqlite3.Connection:
    target = Path(db_path) if db_path is not None else default_db_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(target)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(db_path: str | Path | None = None) -> None:
    with connect(db_path) as connection:
        connection.executescript(SCHEMA_SQL)
        connection.commit()