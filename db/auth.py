"""Authentication, session management, and audit logging.

Stdlib-only: hashlib, secrets, datetime, sqlite3.
"""

from __future__ import annotations

import hashlib
import logging
import secrets
import sqlite3
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)

SESSION_DURATION_DAYS = 7


def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    """Hash a password using SHA-256 with a unique salt."""
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return hashed, salt


def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    """Verify a plain-text password against the stored hash and salt."""
    test_hash, _ = hash_password(password, salt=salt)
    return secrets.compare_digest(test_hash, stored_hash)


def authenticate_user(conn: sqlite3.Connection, username: str, password: str) -> dict | None:
    """Verify credentials and return user info if valid, else None."""
    row = conn.execute(
        "SELECT username, password_hash, salt, display_name, role FROM users WHERE username = ?",
        (username,),
    ).fetchone()
    if not row:
        return None
    if verify_password(password, row["password_hash"], row["salt"]):
        return {
            "username": row["username"],
            "displayName": row["display_name"],
            "role": row["role"],
        }
    return None


def create_session(conn: sqlite3.Connection, username: str) -> str:
    """Create a new session record and return the session ID."""
    session_id = secrets.token_hex(24)
    expires = (datetime.now(tz=timezone.utc) + timedelta(days=SESSION_DURATION_DAYS)).isoformat()
    now = datetime.now(tz=timezone.utc).isoformat()
    conn.execute(
        "INSERT INTO sessions (session_id, username, expires_at, created_at) VALUES (?, ?, ?, ?)",
        (session_id, username, expires, now),
    )
    conn.commit()
    return session_id


def get_user_from_session(conn: sqlite3.Connection, session_id: str) -> dict | None:
    """Look up an active, non-expired session and return the user profile."""
    if not session_id:
        return None
    now = datetime.now(tz=timezone.utc).isoformat()
    row = conn.execute(
        """SELECT u.username, u.display_name, u.role
           FROM sessions s
           JOIN users u ON s.username = u.username
           WHERE s.session_id = ? AND s.expires_at > ?""",
        (session_id, now),
    ).fetchone()
    if row:
        return {
            "username": row["username"],
            "displayName": row["display_name"],
            "role": row["role"],
        }
    return None


def delete_session(conn: sqlite3.Connection, session_id: str) -> None:
    """Invalidate a session."""
    conn.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
    conn.commit()


def count_users(conn: sqlite3.Connection) -> int:
    """Return the total number of registered users."""
    row = conn.execute("SELECT COUNT(*) FROM users").fetchone()
    return row[0] if row else 0


def add_user(
    conn: sqlite3.Connection,
    username: str,
    password: str,
    display_name: str,
    role: str = "coordinator",
) -> None:
    """Register or update a user."""
    p_hash, salt = hash_password(password)
    now = datetime.now(tz=timezone.utc).isoformat()
    conn.execute(
        """INSERT INTO users (username, password_hash, salt, display_name, role, created_at)
           VALUES (?, ?, ?, ?, ?, ?)
           ON CONFLICT(username) DO UPDATE SET
           password_hash = excluded.password_hash,
           salt = excluded.salt,
           display_name = excluded.display_name,
           role = excluded.role""",
        (username, p_hash, salt, display_name, role, now),
    )
    conn.commit()


def record_audit(
    conn: sqlite3.Connection,
    entity: str,
    entity_id: str,
    action: str,
    detail: str,
    user: str,
) -> None:
    """Write an immutable audit log entry."""
    now = datetime.now(tz=timezone.utc).isoformat()
    conn.execute(
        """INSERT INTO audit_events (entity, entity_id, action, detail, user, created_at)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (entity, entity_id, action, detail, user, now),
    )
    conn.commit()
