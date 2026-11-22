"""Database initialisation, WAL mode, migration runner, and nightly backup.

Usage (called once at server startup):
    from db.database import init_db
    init_db(db_path, backup_dir)

The module is intentionally stdlib-only (sqlite3, pathlib, threading, logging).
"""

from __future__ import annotations

import logging
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

_MIGRATIONS_DIR = Path(__file__).parent / "migrations"

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def init_db(db_path: Path | str, backup_dir: Path | str | None = None) -> None:
    """Initialise the database: WAL mode, run pending migrations, start backup thread."""
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with _connect(db_path) as conn:
        _enable_wal(conn)
        _run_migrations(conn)

    if backup_dir is not None:
        backup_path = Path(backup_dir)
        _start_backup_thread(db_path, backup_path)
        logger.info("Nightly backup thread started → %s", backup_path)


def connect(db_path: Path | str) -> sqlite3.Connection:
    """Return a connection with WAL mode and a busy timeout already set."""
    conn = _connect(Path(db_path))
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _connect(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.execute("PRAGMA busy_timeout = 5000")
    return conn


def _enable_wal(conn: sqlite3.Connection) -> None:
    mode = conn.execute("PRAGMA journal_mode=WAL").fetchone()[0]
    logger.info("SQLite journal_mode → %s", mode)
    conn.execute("PRAGMA synchronous=NORMAL")


def _run_migrations(conn: sqlite3.Connection) -> None:
    current_version: int = conn.execute("PRAGMA user_version").fetchone()[0]
    migration_files = sorted(_MIGRATIONS_DIR.glob("*.sql"))

    applied = 0
    for path in migration_files:
        # File name must start with a zero-padded integer version number, e.g. 001_*.sql
        try:
            file_version = int(path.stem.split("_")[0])
        except ValueError:
            logger.warning("Skipping migration file with non-numeric prefix: %s", path.name)
            continue

        if file_version <= current_version:
            continue  # already applied

        logger.info("Applying migration %s …", path.name)
        sql = path.read_text(encoding="utf-8")
        conn.executescript(sql)
        # Update user_version inside a transaction
        conn.execute(f"PRAGMA user_version = {file_version}")
        applied += 1
        logger.info("Migration %s applied (user_version → %d)", path.name, file_version)

    if applied == 0:
        logger.info("Database schema up to date (user_version=%d)", current_version)


# ---------------------------------------------------------------------------
# Nightly backup
# ---------------------------------------------------------------------------

_BACKUP_INTERVAL_SECONDS = 86_400  # 24 hours


def _start_backup_thread(db_path: Path, backup_dir: Path) -> None:
    t = threading.Thread(
        target=_backup_loop,
        args=(db_path, backup_dir),
        daemon=True,
        name="db-backup",
    )
    t.start()


def _backup_loop(db_path: Path, backup_dir: Path) -> None:
    import time

    while True:
        time.sleep(_BACKUP_INTERVAL_SECONDS)
        _run_backup(db_path, backup_dir)


def _run_backup(db_path: Path, backup_dir: Path) -> None:
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
    dest = backup_dir / f"{stamp}.sqlite3"
    try:
        src = sqlite3.connect(str(db_path))
        dst = sqlite3.connect(str(dest))
        with dst:
            src.backup(dst)
        src.close()
        dst.close()
        logger.info("Database backed up → %s", dest)
    except Exception as exc:  # noqa: BLE001
        logger.error("Database backup failed: %s", exc)
