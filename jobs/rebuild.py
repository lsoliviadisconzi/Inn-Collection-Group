"""Rebuild job: runs build_venue_export.py --venue <name> in a subprocess.

Design:
  - One rebuild runs at a time (threading.Lock). A second request while one is
    running returns status immediately without queuing.
  - The job state is kept in memory (server lifetime); it resets on restart.
  - build_menu_explorer.py is run after a successful venue rebuild so the
    menu-explorer-data.js bundle stays in sync.

Public API (called from menu_review_server.py):
    from jobs.rebuild import trigger_rebuild, get_status
"""

from __future__ import annotations

import logging
import subprocess
import sys
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent
_BUILD_VENUE = ROOT / "build_venue_export.py"
_BUILD_EXPLORER = ROOT / "build_menu_explorer.py"

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

StatusLiteral = Literal["idle", "running", "ok", "error"]

_lock = threading.Lock()          # one rebuild at a time
_state_lock = threading.Lock()    # protect _state reads/writes
_state: dict = {
    "status": "idle",
    "venue": None,
    "started_at": None,
    "finished_at": None,
    "error": None,
    "stdout": "",
}


def venue_for_menu(menu_name: str) -> str | None:
    """Find the venue name associated with a given menu markdown file name."""
    try:
        import build_venue_export
        for name, cfg in build_venue_export.VENUES.items():
            if menu_name in cfg.get("menu_files", ()):
                return name
    except Exception as exc:
        logger.warning("Could not resolve venue for menu %s: %s", menu_name, exc)
    return None


def get_status() -> dict:
    """Return a copy of the current job state (safe to serialise as JSON)."""
    with _state_lock:
        return dict(_state)


# ---------------------------------------------------------------------------
# Trigger
# ---------------------------------------------------------------------------

def trigger_rebuild(venue: str) -> dict:
    """Enqueue a rebuild for *venue*.

    Returns the current status dict immediately.
    If a rebuild is already running, returns status without starting another.
    """
    if not _lock.acquire(blocking=False):
        status = get_status()
        status["queued"] = False
        status["message"] = "A rebuild is already running."
        return status

    # We hold the lock — start the job on a background thread.
    _set_state(status="running", venue=venue, started_at=_now(), finished_at=None, error=None, stdout="")
    t = threading.Thread(target=_run, args=(venue,), daemon=True, name=f"rebuild-{venue}")
    t.start()

    return get_status()


# ---------------------------------------------------------------------------
# Worker
# ---------------------------------------------------------------------------

def _run(venue: str) -> None:
    try:
        logger.info("Rebuild started: venue=%r", venue)
        out_lines: list[str] = []

        # Step 1: venue export
        extra_args = ["--all"] if venue.lower() == "all" else ["--venue", venue]
        ok = _run_script(_BUILD_VENUE, extra_args, out_lines)

        # Step 2: explorer bundle (only if venue export succeeded)
        if ok:
            _run_script(_BUILD_EXPLORER, [], out_lines)

        stdout = "\n".join(out_lines)
        if ok:
            logger.info("Rebuild finished OK: venue=%r", venue)
            _set_state(status="ok", finished_at=_now(), stdout=stdout)
        else:
            logger.error("Rebuild failed: venue=%r", venue)
            _set_state(status="error", finished_at=_now(), stdout=stdout,
                       error="Build script exited with a non-zero status. See stdout for details.")
    except Exception as exc:  # noqa: BLE001
        logger.exception("Rebuild job raised an exception: venue=%r", venue)
        _set_state(status="error", finished_at=_now(), error=str(exc))
    finally:
        _lock.release()


def _run_script(script: Path, extra_args: list[str], out_lines: list[str]) -> bool:
    """Run *script* as a subprocess, capturing stdout+stderr. Returns True on success."""
    cmd = [sys.executable, str(script)] + extra_args
    logger.debug("Running: %s", " ".join(cmd))
    result = subprocess.run(
        cmd,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=300,   # 5-minute hard limit
    )
    combined = result.stdout + result.stderr
    if combined.strip():
        out_lines.extend(combined.splitlines())
    return result.returncode == 0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def _set_state(**kwargs) -> None:
    with _state_lock:
        _state.update(kwargs)
